from django.db import models

# Create your models here.

class Person(models.Model):
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    address = models.ForeignKey("Address", related_name="people")

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)

class Address(models.Model):
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    house_nr = models.IntegerField()
    flat_nr = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "{}, {} {} {}".format(self.city, self.street, self.house_nr, self.flat_nr)

TYPES = (
    (1, "home"),
    (2, "business")
)

class Phone(models.Model):
    number = models.IntegerField()
    type = models.IntegerField(choices=TYPES)
    owner = models.ForeignKey(Person, related_name="phones")

    def __str__(self):
        return "{}: {}".format(self.type, self.number)


class Email(models.Model):
    email = models.CharField(max_length=64)
    type = models.IntegerField(choices=TYPES)
    owner = models.ForeignKey(Person, related_name='emails')

    def __str__(self):
        return "{} {}".format(self.email, self.type)

class Group(models.Model):
    name = models.CharField(max_length=256)
    member = models.ManyToManyField(Person, related_name='groups')

    def __str__(self):
        return self.name

