from django.db.models import *


class Author(Model):
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(Model):
    author = ForeignKey(Author, on_delete=PROTECT, related_name="books")

    title = CharField(max_length=255)

    def __str__(self):
        return f"{self.title} by {self.author}"
