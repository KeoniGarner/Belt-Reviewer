from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def validations(self, post_data):
        valid = True
        errors = {}
        if len(post_data["name"]) < 2:
            valid = False
            errors["name"] = "Name must be longer than 2 characters!"
        if len(post_data["alias"]) < 2:
            valid = False
            errors["alias"] = "Alias must be longer than 2 characters!"
        if len(post_data["reg_email"]) < 7:
            valid = False
            errors["email"] = "Email must be more than 7 characters!"
        if "@" not in post_data["reg_email"] or "." not in post_data["reg_email"]:
            valid = False
            errors["email"] = "Email must be a valid email address!"
        if not re.match(r"^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))", post_data["reg_password"]):
            valid = False
            errors["password"] = "Password must contain at least one uppercase and one numeric character."
        if not post_data["reg_password"] == post_data["confirm"]:
            valid = False
            errors["confirm"] = "Passwords must match."
        return (valid, errors)

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    rating = models.IntegerField(default = 3)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Author(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name="authors")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)