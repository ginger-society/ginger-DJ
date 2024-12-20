from gingerdj.db import models


class Award(models.Model):
    name = models.CharField(max_length=25)
    object_id = models.PositiveIntegerField()


class AwardNote(models.Model):
    award = models.ForeignKey(Award, models.CASCADE)
    note = models.CharField(max_length=100)


class Person(models.Model):
    name = models.CharField(max_length=25)


class Book(models.Model):
    pagecount = models.IntegerField()
    owner = models.ForeignKey("Child", models.CASCADE, null=True)


class Toy(models.Model):
    name = models.CharField(max_length=50)


class Child(models.Model):
    name = models.CharField(max_length=50)
    toys = models.ManyToManyField(Toy, through="PlayedWith")


class PlayedWith(models.Model):
    child = models.ForeignKey(Child, models.CASCADE)
    toy = models.ForeignKey(Toy, models.CASCADE)
    date = models.DateField(db_column="date_col")


class PlayedWithNote(models.Model):
    played = models.ForeignKey(PlayedWith, models.CASCADE)
    note = models.TextField()


class Contact(models.Model):
    label = models.CharField(max_length=100)


class Email(Contact):
    email_address = models.EmailField(max_length=100)


class Researcher(models.Model):
    contacts = models.ManyToManyField(Contact, related_name="research_contacts")
    primary_contact = models.ForeignKey(
        Contact, models.SET_NULL, null=True, related_name="primary_contacts"
    )
    secondary_contact = models.ForeignKey(
        Contact, models.SET_NULL, null=True, related_name="secondary_contacts"
    )


class Food(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Eaten(models.Model):
    food = models.ForeignKey(Food, models.CASCADE, to_field="name")
    meal = models.CharField(max_length=20)


# Models for #15776


class Policy(models.Model):
    policy_number = models.CharField(max_length=10)


class Version(models.Model):
    policy = models.ForeignKey(Policy, models.CASCADE)


class Location(models.Model):
    version = models.ForeignKey(Version, models.SET_NULL, blank=True, null=True)


class Item(models.Model):
    version = models.ForeignKey(Version, models.CASCADE)
    location = models.ForeignKey(Location, models.SET_NULL, blank=True, null=True)
    location_value = models.ForeignKey(
        Location, models.SET(42), default=1, db_constraint=False, related_name="+"
    )


# Models for #16128


class File(models.Model):
    pass


class Image(File):
    class Meta:
        proxy = True


class Photo(Image):
    class Meta:
        proxy = True


class FooImage(models.Model):
    my_image = models.ForeignKey(Image, models.CASCADE)


class FooFile(models.Model):
    my_file = models.ForeignKey(File, models.CASCADE)


class FooPhoto(models.Model):
    my_photo = models.ForeignKey(Photo, models.CASCADE)


class FooFileProxy(FooFile):
    class Meta:
        proxy = True


class OrgUnit(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Login(models.Model):
    description = models.CharField(max_length=32)
    orgunit = models.ForeignKey(OrgUnit, models.CASCADE)


class House(models.Model):
    address = models.CharField(max_length=32)


class OrderedPerson(models.Model):
    name = models.CharField(max_length=32)
    lives_in = models.ForeignKey(House, models.CASCADE)

    class Meta:
        ordering = ["name"]


def get_best_toy():
    toy, _ = Toy.objects.get_or_create(name="best")
    return toy


def get_worst_toy():
    toy, _ = Toy.objects.get_or_create(name="worst")
    return toy


class Collector(models.Model):
    best_toy = models.ForeignKey(
        Toy, default=get_best_toy, on_delete=models.SET_DEFAULT, related_name="toys"
    )
    worst_toy = models.ForeignKey(
        Toy, models.SET(get_worst_toy), related_name="bad_toys"
    )
