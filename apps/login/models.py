from __future__ import unicode_literals

from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import hashlib
import binascii
from os import urandom

class UserManager(models.Manager):
    def get_users(self):
        response_to_views = User.objects.all()
        return response_to_views

    def remove_user(self, id):
        response_to_views = User.objects.get(id=id).delete()
        return response_to_views

    def edit_validation(self, postData, user):
        errors = []

        if len(postData['firstname']) < 1:
            errors.append("First name field cannot be blank.")

        if len(postData['lastname']) < 1:
            errors.append("Last name field cannot be blank.")

        if len(postData['email']) < 1:
            errors.append("Email field cannot be blank.")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Email address is not valid.")

        # Existing email validation should go here

        response_to_views = {}
        if errors:
            response_to_views['status'] = False
            response_to_views['error'] = errors
        else:
            user.email = postData['email']
            user.firstname = postData['firstname']
            user.lastname = postData['lastname']
            if postData['status'] == 'admin':
                user.admin = True
            if postData['status'] == 'user':
                user.admin = False
            user.save()
            response_to_views['status'] = True
            response_to_views['user'] = user
        return response_to_views

    def password_edit_validation(self, postData, user):
        errors = []

        if len(postData['password']) < 4:
            errors.append("Password must be at least 4 charaters.")
        if len(postData['confirm']) < 1:
            errors.append("Please confirm your password.")
        if not postData["password"] == postData["confirm"]:
            errors.append("Your passwords do not match.")

        response_to_views = {}
        if errors:
            response_to_views['status'] = False
            response_to_views['error'] = errors
        else:
            hashed_password = hashlib.md5(postData['password'].encode('utf-8')).hexdigest();
            user.password = hashed_password
            user.save()
            response_to_views['status'] = True
            response_to_views['user'] = user
        return response_to_views

    def edit_profile(self, postData, user):
        errors = []

        if len(postData['firstname']) < 1:
            errors.append("First name field cannot be blank.")

        if len(postData['lastname']) < 1:
            errors.append("Last name field cannot be blank.")

        if len(postData['email']) < 1:
            errors.append("Email field cannot be blank.")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Email address is not valid.")

        # Existing email validation should go here

        response_to_views = {}
        if errors:
            response_to_views['status'] = False
            response_to_views['error'] = errors
        else:
            user.email = postData['email']
            user.firstname = postData['firstname']
            user.lastname = postData['lastname']
            user.save()
            response_to_views['status'] = True
            response_to_views['user'] = user
        return response_to_views

    def edit_user_password(self, postData, user):
        errors = []

        if len(postData['password']) < 4:
            errors.append("Password must be at least 4 charaters.")
        if len(postData['confirm']) < 1:
            errors.append("Please confirm your password")
        if not postData["password"] == postData["confirm"]:
            errors.append("Your passwords do not match")

        response_to_views = {}
        if errors:
            response_to_views['status'] = False
            response_to_views['error'] = errors
        else:
            hashed_password = hashlib.md5(postData['password'].encode('utf-8')).hexdigest();
            user.password = hashed_password
            user.save()
            response_to_views['status'] = True
            response_to_views['user'] = user
        return response_to_views

    def edit_description(self, postData, user):

        response_to_views = {}
        user.description = postData['description']
        user.save()
        response_to_views['user'] = user
        return response_to_views

    def user_validation(self, postData):
        errors = []

        if len(postData['first_name']) < 1:
            errors.append("First name field cannot be blank.")

        if len(postData['last_name']) < 1:
            errors.append("Last name field cannot be blank.")

        if len(postData['email']) < 1:
            errors.append("Email field cannot be blank.")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Email address is not valid.")
        try:
            User.objects.get(email = postData['email'])
            errors.append("Email has already been registered")
        except:
            pass

        if len(postData['password']) < 4:
            errors.append("Password must be at least 4 characters.")
        if len(postData['confirm']) < 1:
            errors.append("Please confirm your password.")
        if not postData["password"] == postData["confirm"]:
            errors.append("Your passwords do not match.")


        response_to_views = {}
        if errors:
            response_to_views['status'] = False
            response_to_views['error'] = errors
        else:
            hashed_password = hashlib.md5(postData['password'].encode('utf-8')).hexdigest();
            user = self.create(firstname=postData['first_name'], lastname=postData['last_name'], email=postData['email'], password=hashed_password)
            if user.email == "bradvsherman@gmail.com":
                user.admin = True
                user.save()
            response_to_views['status'] = True
            response_to_views['user'] = user
        return response_to_views

    def login_validation(self, postData):

        login_errors = []
        hashed_password = hashlib.md5(postData['password'].encode('utf-8')).hexdigest();

        try:
            User.objects.get(email=postData["email"])
        except:
            login_errors.append("Email incorrect.")
        try:
            User.objects.get(email=postData["email"], password=hashed_password)
        except:
            login_errors.append("Password incorrect.")

        response_to_views = {}
        if login_errors:
            response_to_views['status'] = False
            response_to_views['errors'] = login_errors
        else:
            user = User.objects.get(email=postData["email"])
            response_to_views['status'] = True
            response_to_views['user'] = user
        return response_to_views

class User(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    password = models.CharField(max_length = 100)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
