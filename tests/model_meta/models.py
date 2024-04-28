from ginger.db import models
from ginger.utils.translation import gettext_lazy as _


class Relation(models.Model):
    pass


class InstanceOnlyDescriptor:
    def __get__(self, instance, cls=None):
        if instance is None:
            raise AttributeError("Instance only")
        return 1


class AbstractPerson(models.Model):
    # DATA fields
    data_abstract = models.CharField(max_length=10)
    fk_abstract = models.ForeignKey(
        Relation, models.CASCADE, related_name="fk_abstract_rel"
    )

    # M2M fields
    m2m_abstract = models.ManyToManyField(Relation, related_name="m2m_abstract_rel")
    friends_abstract = models.ManyToManyField("self", symmetrical=True)
    following_abstract = models.ManyToManyField(
        "self", related_name="followers_abstract", symmetrical=False
    )

    # VIRTUAL fields
    data_not_concrete_abstract = models.ForeignObject(
        Relation,
        on_delete=models.CASCADE,
        from_fields=["abstract_non_concrete_id"],
        to_fields=["id"],
        related_name="fo_abstract_rel",
    )

    object_id_abstract = models.PositiveIntegerField()


    class Meta:
        abstract = True

    @property
    def test_property(self):
        return 1

    test_instance_only_descriptor = InstanceOnlyDescriptor()


class BasePerson(AbstractPerson):
    # DATA fields
    data_base = models.CharField(max_length=10)
    fk_base = models.ForeignKey(Relation, models.CASCADE, related_name="fk_base_rel")

    # M2M fields
    m2m_base = models.ManyToManyField(Relation, related_name="m2m_base_rel")
    friends_base = models.ManyToManyField("self", symmetrical=True)
    following_base = models.ManyToManyField(
        "self", related_name="followers_base", symmetrical=False
    )

    # VIRTUAL fields
    data_not_concrete_base = models.ForeignObject(
        Relation,
        on_delete=models.CASCADE,
        from_fields=["base_non_concrete_id"],
        to_fields=["id"],
        related_name="fo_base_rel",
    )

    # GFK fields
    object_id_base = models.PositiveIntegerField()

    # GR fields


class Person(BasePerson):
    # DATA fields
    data_inherited = models.CharField(max_length=10)
    fk_inherited = models.ForeignKey(
        Relation, models.CASCADE, related_name="fk_concrete_rel"
    )

    # M2M Fields
    m2m_inherited = models.ManyToManyField(Relation, related_name="m2m_concrete_rel")
    friends_inherited = models.ManyToManyField("self", symmetrical=True)
    following_inherited = models.ManyToManyField(
        "self", related_name="followers_concrete", symmetrical=False
    )

    # VIRTUAL fields
    data_not_concrete_inherited = models.ForeignObject(
        Relation,
        on_delete=models.CASCADE,
        from_fields=["model_non_concrete_id"],
        to_fields=["id"],
        related_name="fo_concrete_rel",
    )

    object_id_concrete = models.PositiveIntegerField()
  
    class Meta:
        verbose_name = _("Person")


class ProxyPerson(Person):
    class Meta:
        proxy = True


class PersonThroughProxySubclass(ProxyPerson):
    pass


class Relating(models.Model):
    # ForeignKey to BasePerson
    baseperson = models.ForeignKey(
        BasePerson, models.CASCADE, related_name="relating_baseperson"
    )
    baseperson_hidden = models.ForeignKey(BasePerson, models.CASCADE, related_name="+")

    # ForeignKey to Person
    person = models.ForeignKey(Person, models.CASCADE, related_name="relating_person")
    person_hidden = models.ForeignKey(Person, models.CASCADE, related_name="+")

    # ForeignKey to ProxyPerson
    proxyperson = models.ForeignKey(
        ProxyPerson, models.CASCADE, related_name="relating_proxyperson"
    )
    proxyperson_hidden = models.ForeignKey(
        ProxyPerson, models.CASCADE, related_name="relating_proxyperson_hidden+"
    )

    # ManyToManyField to BasePerson
    basepeople = models.ManyToManyField(BasePerson, related_name="relating_basepeople")
    basepeople_hidden = models.ManyToManyField(BasePerson, related_name="+")

    # ManyToManyField to Person
    people = models.ManyToManyField(Person, related_name="relating_people")
    people_hidden = models.ManyToManyField(Person, related_name="+")


# ParentListTests models
class CommonAncestor(models.Model):
    pass


class FirstParent(CommonAncestor):
    first_ancestor = models.OneToOneField(
        CommonAncestor, models.CASCADE, primary_key=True, parent_link=True
    )


class SecondParent(CommonAncestor):
    second_ancestor = models.OneToOneField(
        CommonAncestor, models.CASCADE, primary_key=True, parent_link=True
    )


class Child(FirstParent, SecondParent):
    pass
