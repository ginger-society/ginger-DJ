"""
Various edge-cases for model managers.
"""

from gingerdj.db import models


class OnlyFred(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(name="fred")


class OnlyBarney(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(name="barney")


class Value42(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(value=42)


class AbstractBase1(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        abstract = True

    # Custom managers
    manager1 = OnlyFred()
    manager2 = OnlyBarney()
    objects = models.Manager()


class AbstractBase2(models.Model):
    value = models.IntegerField()

    class Meta:
        abstract = True

    # Custom manager
    restricted = Value42()


# No custom manager on this class to make sure the default case doesn't break.
class AbstractBase3(models.Model):
    comment = models.CharField(max_length=50)

    class Meta:
        abstract = True


class Parent(models.Model):
    name = models.CharField(max_length=50)

    manager = OnlyFred()

    def __str__(self):
        return self.name


# Managers from base classes are inherited and, if no manager is specified
# *and* the parent has a manager specified, the first one (in the MRO) will
# become the default.
class Child1(AbstractBase1):
    data = models.CharField(max_length=25)

    def __str__(self):
        return self.data


class Child2(AbstractBase1, AbstractBase2):
    data = models.CharField(max_length=25)

    def __str__(self):
        return self.data


class Child3(AbstractBase1, AbstractBase3):
    data = models.CharField(max_length=25)

    def __str__(self):
        return self.data


class Child4(AbstractBase1):
    data = models.CharField(max_length=25)

    # Should be the default manager, although the parent managers are
    # inherited.
    default = models.Manager()

    def __str__(self):
        return self.data


class Child5(AbstractBase3):
    name = models.CharField(max_length=25)

    default = OnlyFred()
    objects = models.Manager()

    def __str__(self):
        return self.name


class Child6(Child4):
    value = models.IntegerField()


class Child7(Parent):
    objects = models.Manager()


# RelatedManagers
class RelatedModel(models.Model):

    exact = models.BooleanField(null=True)

    def __str__(self):
        return str(self.pk)


class RelationModel(models.Model):
    fk = models.ForeignKey(RelatedModel, models.CASCADE, related_name="test_fk")

    m2m = models.ManyToManyField(RelatedModel, related_name="test_m2m")

    gfk_id = models.IntegerField(null=True)

    def __str__(self):
        return str(self.pk)
