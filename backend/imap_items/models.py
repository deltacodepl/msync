import csv
from io import StringIO
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
            print(type(self.csv_file.open(mode='r').readlines()))
            csv_data: list = csv.reader(StringIO(self.csv_file.open(mode='r').read().decode('utf-8')))
            
            for item in csv_data:
                print(item)
            print('Success')
        except Exception as e:
            print('CSV failed:', e)

        return super().save(*args, **kwargs)
