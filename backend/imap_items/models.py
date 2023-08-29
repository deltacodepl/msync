import csv

from django.db import models
from PIL import Image


class ImapItem(models.Model):
    csv_file = models.FileField(upload_to='files')
    result = models.CharField(max_length=250, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'File uploaded at {}'.format(self.date_uploaded.strftime('%Y-%m-%d %H:%M'))

    def save(self, *args, **kwargs):
        try:

            self.result = str("decoded")
            csv_data = csv.reader(self.csv_file.open(mode='rb'))
            for item in csv_data:
                print(item)
            print('Success')
        except Exception as e:
            print('Classification failed:', e)

        return super().save(*args, **kwargs)
