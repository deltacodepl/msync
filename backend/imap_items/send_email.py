import os
import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s %(module)s "
    "%(process)s[%(thread)s] %(message)s",
)


def render_template(template, data):
    """renders a Jinja template into HTML"""
    # check if template exists

    # if not os.path.exists(f"../templates/{template}"):
    #     logger.error("No template file present: %s" % template)
    #     sys.exit()

    import jinja2

    template_loader = jinja2.FileSystemLoader(searchpath="/app/templates/")
    template_env = jinja2.Environment(loader=template_loader)
    templ = template_env.get_template(template)
    return templ.render(data)


# ------------------------------------------------------------------------------------------------
def send_email(
    to,
    sender=None,
    cc=None,
    bcc=None,
    subject=None,
    body=None,
):
    """sends email using a Jinja HTML template"""
    import smtplib

    # Import the email modules
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.header import Header
    from email.utils import formataddr

    # convert TO into list if string
    if type(to) is not list:
        to = to.split()

    to_list = to + [cc] + [bcc]
    to_list = list(filter(None, to_list))  # remove null emails

    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["Subject"] = subject
    msg["To"] = ",".join(to)
    msg["Cc"] = cc
    msg["Bcc"] = bcc
    msg.attach(MIMEText(body, "html"))
    server = smtplib.SMTP("poczta.pl", 587)
    server.starttls()
    try:
        server.login("", "")
        server.sendmail(sender, to_list, msg.as_string())
    except Exception as e:
        logger.error("Error sending email")
        logger.exception(str(e))
    finally:
        logger.info(f"email sent: {msg['To']}")
        server.quit()


# ------------------------------------------------------------------------------------------------
#
# if __name__ == '__main__':
#     returncode = 0
#     to_email = "testowe"
#
#     message_to_user = {
#         "result": "json.dumps(result)",
#         "subject": ("Nowe konto pocztowe %s" % ("zostało utworzone" if returncode == 0 else "failure")),
#         "from": "KO<>",
#         "to": to_email,
#         "username": to_email,
#         "password": "password",
#         "host": "poczta.pl",
#     }
#     # generate HTML from template
#     html = render_template("email.j2", message_to_user)
#
#     to_list = [message_to_user.get('to')]
#     sender = "KO<>"
#     cc = ""
#     subject = message_to_user.get('subject')
#
#     # send email to a list of email addresses
#     send_email(to_list, sender, cc, None, subject, html)
