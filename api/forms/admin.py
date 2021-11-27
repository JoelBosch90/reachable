from django.contrib import admin

# Get the models definitions.
from .models import User, Form, Link, Input
models = [User, Form, Link, Input]

# Register your models here.
admin.site.register(models)
