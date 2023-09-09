# coding: utf-8
import json
import pprint
import smtplib
import sys
from celery import shared_task
from celery.utils.log import get_task_logger
from email.mime.text import MIMEText
from subprocess import PIPE, Popen
from threading import Thread
from queue import Queue, Empty
from .sqs import send_message

logger = get_task_logger(__name__)

ON_POSIX = 'posix' in sys.builtin_module_names


def enqueue_output(output_line, queue):
    for line in iter(output_line.readline, b''):
        logger.info(f"Line: {line.decode('utf-8')}")
        queue.put(line.decode('utf-8'))
    queue.task_done()
    output_line.close()


def get_imapsync_host_args(i, host):
    if not all(host.get(x) for x in ('host', 'user', 'password')):
        raise ValueError('Missing value for host')

    args = [
        '--host%d' % i, host['host'],
        '--user%d' % i, host['user'],
        # '--password%d' % i, f"'{host['password']}'",
        '--password%d' % i, host['password'],
    ]

    if host.get('encryption') == 'tls':
        args.append('--tls%d' % i)
    elif host.get('encryption') == 'ssl':
        args.append('--ssl%d' % i)

    return args


@shared_task(bind=True)
def imapsync(self, host1, host2, options={}):
    """
    Run imap synchronization.
    """
    # Start imapsync
    logger.info('Starting Syncer from %s@%s to %s@%s with %r', host1['user'],
                host1['host'], host2['user'], host2['host'], options)
    
    command = (['imapsync', '--nolog', '--noreleasecheck', '--automap'] +
               get_imapsync_host_args(1, host1) +
               get_imapsync_host_args(2, host2))

    process = Popen(command, stdout=PIPE, bufsize=1, close_fds=ON_POSIX)

    # Open a queue to put the output of imapsync
    q = Queue()
    q.put('++++ Started\n')

    # Start the thread that reads the output
    t = Thread(target=enqueue_output, args=(process.stdout, q))
    t.daemon = True
    t.start()

    # read output
    result: dict = {}
    state = None
    while True:
        try:
            line: str = q.get(timeout=5)
        except Empty:
            if not t.is_alive():
                break
        else:  # got line
            logger.info(f"Imap Line: {type(line)} - {line}")

            line: str = line.rstrip()

            if line.startswith('++++ '):
                if line.startswith('++++ Calculating sizes on Host'):
                    state = 'CALCULATING'
                elif line == '++++ Listing folders':
                    state = 'LISTING'
                elif line == '++++ Looping on each folder':
                    state = 'SYNCING'
                elif line == '++++ Statistics':
                    state = 'STATISTICS'
                else:
                    try:
                        state = line.split()[1].upper()
                    except IndexError:
                        pass

                logger.info('Changed state to %s', state)
                self.update_state(state=state)
            elif state == 'STATISTICS':
                if ':' in line:
                    key, value = line.split(':', 1)
                    result[key.strip()] = value.strip()

    # Set the output status
    process.wait()

    # Store the resultcode
    result['returncode'] = process.returncode
    logger.info('Syncer completed with %s %s', result.get('Folders synced'),
                'success' if process.returncode == 0 else 'failure')

    to_email = host1['user']
    password = host2['password']
    host = host2['host']
    from_email = 'marketing@segregatory24.pl'

    logger.info('Sending feedback email to %s from %s', to_email,
                from_email)

    message_to_user = {'result': json.dumps(result),
                       'subject': ('New email account setup completed with %s' % ('success' if process.returncode == 0 else 'failure')),
                       'from': from_email,
                       'to': to_email,
                       'password': password,
                       'host': host,
                       }
    send_message(message=message_to_user)

    # if options.get('feedback_to_email') and options.get('feedback_from_email'):
    #     self.update_state(state='SENDING_FEEDBACK_EMAIL')
        # s = smtplib.SMTP('localhost')
        # s.sendmail(from_email, [to_email], message.as_string())
        # s.quit()

    return result
