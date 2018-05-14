from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

# Create your models here.

class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = {}
        # Check to see if email exists in database
        if len(User.objects.filter(email=postData['email']))==0:
            errors['email'] = "That email has not been registered with us. Try again or register above."
        else:
        # Check hashed bcrypt password submitted is equal to the encoded stored hash
            if not bcrypt.checkpw(postData['password'].encode(), User.objects.get(email=postData['email']).password.encode()):
                errors['password'] = "Password incorrect. Try again."
        
        return errors

    def register_validator(self, postData):
        errors = {}
        # Required Validation
        if postData['first_name'] is None or postData['last_name'] is None or postData['email'] is None or postData['password'] is None:
            errors['required'] = "All fields are required."
        else:
            # Name LENGTH Validation
            if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
                errors['name_length'] = "User first and last name should be at least 2 letters long."
            # Name ALL-ALPHA Validation
            if not re.match(r"[a-zA-Z]+", postData['first_name']) or not re.match(r"[a-zA-Z]+", postData['last_name']):
                errors['name_alpha'] = "User's name must be alphabet."
            # Email Validation
            if len(User.objects.filter(email=postData['email']))>0:
                errors['email_dup'] = "This email has already been registered previously. Login instead."
            if not re.match(r"([\w.-]+@([\w-]+)\.+\w{2,})", postData['email']):
                errors['email'] = "Please verify your email address is in format xxx@xxx.com."
            # Password Validation
            if len(postData['password']) < 8:
                errors['pw_length'] = "Password must be at least 8 characters in length."
            # password to confirm validation
            if postData['password'] != postData['confirm']:
                errors['pw_confirm'] = "Confirmation does not match password. Try again."
        return errors
    

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

# Show validation error messages if validations fail the following tests
# First Name - Required; No fewer than 2 characters; letters only
# Last Name - Required; No fewer than 2 characters; letters only [a-z]
# Email - Required; Valid Format
# Password - Required; No fewer than 8 characters in length; matches Password Confirmation