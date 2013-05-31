from foo.models import Publisher
from foo.models import Author
from foo.models import Book

from django.contrib import admin
from django.contrib.auth.models import User

admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Book)