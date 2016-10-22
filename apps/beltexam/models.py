from __future__ import unicode_literals
import bcrypt

from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def login(self, post):
        user_list = User.objects.filter(username=post['username'])
        if user_list:
            user = user_list[0]
            #check their credentials
            if bcrypt.hashpw(post['password'].encode(), user.password.encode()) == user.password:
                #then login is valid
                return user
        #else:
        return None

    def register(self, post):
        encrypted_password = bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt())
        User.objects.create(name=post['name'], username=post['username'], password=encrypted_password)

    def validate_user_info(self, post):
        errors = []

        if len(post['name']) < 3:
            errors.append('Name must contain at least 3 characters!')
        # if not post['firstname'].isalpha():
        #     errors.append('All First Name characters must be alphabetic!.')
        if len(post['username']) == 0:
            errors.append('Username cannot be blank!')

        if len(post['password']) < 8:
            errors.append('Your password must contain at least 8 characters!')
        if post['password'] != post['confpass']:
            errors.append('Your confirmation password must match your password!')

        return errors

class TripManager(models.Manager):
    pass

class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Trip(models.Model):
    user = models.ForeignKey(User)
    destination = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    start = models.IntegerField()
    end = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripManager
