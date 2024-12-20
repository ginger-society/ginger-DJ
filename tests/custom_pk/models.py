"""
Using a custom primary key

By default, GingerDJ adds an ``"id"`` field to each model. But you can override
this behavior by explicitly adding ``primary_key=True`` to a field.
"""

from gingerdj.db import models

from .fields import MyAutoField, MyWrapperField


class Employee(models.Model):
    employee_code = models.IntegerField(primary_key=True, db_column="code")
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    class Meta:
        ordering = ("last_name", "first_name")

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Business(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    employees = models.ManyToManyField(Employee)

    class Meta:
        verbose_name_plural = "businesses"


class Bar(models.Model):
    id = MyWrapperField(primary_key=True, db_index=True)


class Foo(models.Model):
    bar = models.ForeignKey(Bar, models.CASCADE)


class CustomAutoFieldModel(models.Model):
    id = MyAutoField(primary_key=True)
