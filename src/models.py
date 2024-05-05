from ginger.db import models

# Create your models here.


class Tenant2(models.Model):
    """Tenant model , this is equivalent to an organization or BU unit"""

    name = models.CharField(max_length=200, unique=True)
    name2 = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(default=True)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "shared_tenant2"


CHOICES = (
    ("choice1", "choice1"),
    ("choice2", "choice2"),
    ("choice3", "choice3"),
)

class Test(models.Model):
    """test"""

    choice_field = models.CharField(null=True, choices=CHOICES, max_length=50, default="choice1")
    bool_field = models.BooleanField(default=True)
    char_field = models.CharField(null=True, max_length=50)
    positive_integer_field = models.PositiveIntegerField(null=False, default=0)
    field3 = models.BooleanField(default=False)

    class Meta:
        db_table = "test"


class TestAppModel1(models.Model):
    """test app model"""

    char_field = models.CharField(max_length=200, null=False)

    class Meta:
        db_table = "testAppModel1"


class Many2ManyTest(models.Model):
    """m2m test"""

    name = models.CharField(max_length=200, null=False)
    testModels = models.ManyToManyField(Test, related_name="main_models")
    crossAppModel = models.ManyToManyField(TestAppModel1, related_name="cross_app_m2mtest")

    class Meta:
        db_table = "many2ManyTest"