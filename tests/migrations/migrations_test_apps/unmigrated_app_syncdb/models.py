from gingerdj.db import models


class Classroom(models.Model):
    pass


class Lesson(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
