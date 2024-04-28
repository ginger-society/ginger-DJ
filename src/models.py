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