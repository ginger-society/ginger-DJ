from gingerdj.db import models


class FileModel(models.Model):
    testfile = models.FileField(upload_to="test_upload")
