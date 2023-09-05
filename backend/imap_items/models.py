import csv
from io import StringIO
from django.db import models
from .tasks import imapsync


def split_csv(row: dict):
    """
    {'host1': 'properpack.nazwa.pl', 'user1': 'testowe@properline.pl', 'password1': '@',
     'host2': 'poczta23126.e-kei.pl', 'user2': 'testowe@properline.pl', 'password2': '@'}
    """
    keys = ('host', 'user', 'password')
    host1 = dict(zip(keys, list(row.values())[:3]))
    host2 = dict(zip(keys, list(row.values())[3:]))

    return host1, host2


class ImapItem(models.Model):
    csv_file = models.FileField(upload_to="files")
    result = models.CharField(max_length=250, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "File uploaded at {}".format(
            self.date_uploaded.strftime("%Y-%m-%d %H:%M")
        )

    def save(self, *args, **kwargs):
        try:
            self.result = str("decoded")

            # print(type(self.csv_file.open(mode='r').readlines()))

            # iterator over the csv rows
            csv_data = csv.DictReader(
                StringIO(self.csv_file.open(mode="r").read().decode("utf-8"))
            )

            for row in csv_data:
                # print(row)
                print(split_csv(row))
                imapsync.delay(*split_csv(row))

            print("Success")

        except Exception as e:
            print("CSV failed:", e)

        return super().save(*args, **kwargs)
