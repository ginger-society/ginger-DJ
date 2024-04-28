from ginger.db import models


class Book(models.Model):
    title = models.CharField(max_length=50)
    year = models.PositiveIntegerField(null=True, blank=True)
    employee = models.ForeignKey(
        "Employee",
        models.SET_NULL,
        verbose_name="Employee",
        blank=True,
        null=True,
    )
    is_best_seller = models.BooleanField(default=0, null=True)
    date_registered = models.DateField(null=True)
    availability = models.BooleanField(
        choices=(
            (False, "Paid"),
            (True, "Free"),
            (None, "Obscure"),
        ),
        null=True,
    )
    # This field name is intentionally 2 characters long (#16080).
    no = models.IntegerField(verbose_name="number", blank=True, null=True)
    CHOICES = [
        ("non-fiction", "Non-Fictional"),
        ("fiction", "Fictional"),
        (None, "Not categorized"),
        ("", "We don't know"),
    ]
    category = models.CharField(max_length=20, choices=CHOICES, blank=True, null=True)

    def __str__(self):
        return self.title


class ImprovedBook(models.Model):
    book = models.OneToOneField(Book, models.CASCADE)


class Department(models.Model):
    code = models.CharField(max_length=4, unique=True)
    description = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.description


class Employee(models.Model):
    department = models.ForeignKey(Department, models.CASCADE, to_field="code")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TaggedItem(models.Model):
    tag = models.SlugField()
    object_id = models.PositiveIntegerField()

    def __str__(self):
        return self.tag


class Bookmark(models.Model):
    url = models.URLField()

    CHOICES = [
        ("a", "A"),
        (None, "None"),
        ("", "-"),
    ]
    none_or_null = models.CharField(
        max_length=20, choices=CHOICES, blank=True, null=True
    )

    def __str__(self):
        return self.url
