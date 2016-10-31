from __future__ import unicode_literals
from django.db import models
import bcrypt
import datetime
import re

now = datetime.datetime.now()
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def login(self, email_in, pwd_in):
        error = False
        if len(email_in) < 2:
            error = True

        if not EMAIL_REGEX.match(email_in):
            error = True  # END OF EMAIL VALIDATION

        if len(pwd_in) < 8:
            error = True  # END OF PASSWORD VALIDATION

        if error is True:
            return False
        else:
            passwordHash = Users.UserManager.filter(email=email_in).last().password.encode()
            if bcrypt.hashpw(pwd_in, passwordHash) == passwordHash:
                return True
            else:
                return False

    def register(self, name_up, username_up, email_up, pwd_up):
        error = []
        if len(username_up) < 2:
            error.append("Too short!! Username should be at least 2 characters")
        elif not username_up:
            error.append("Username field must be filled out")  # END OF FIRST NAME VALIDATION

        if len(name_up) < 2:
            error.append("Please enter your full name")  # END OF EMAIL VALIDATION

        if not EMAIL_REGEX.match(email_up):
            error.append("Email is in wrong format")  # END OF EMAIL VALIDATION

        if len(pwd_up) < 8:
            error.append('Password is too short')
        if len(error) > 0:
            return [False, error]
        else:
            hashedPW = bcrypt.hashpw(pwd_up, bcrypt.gensalt())
            Users.UserManager.create(name=name_up, username=username_up, email=email_up, password=hashedPW,
                                     created_at=now)
            return [True]

    def validuser(self, username_valid):
        if len(username_valid) < 3:
            return True
        else:
            return False

    def validemail(self, email_valid):
        if not EMAIL_REGEX.match(email_valid):
            return True
        else:
            return False

    def validpassword(self, pass_valid):
        if len(pass_valid) < 9:
            return True
        else:
            return False

    def matchpasswords(self, password, confirmpass):
        if password != confirmpass:
            return True
        else:
            return False


class QuoteManager(models.Manager):
    def addQuote(self, quoted_by, newMsg, user):
        error = []
        if len(quoted_by) < 3:
            error.append("Too short!! Quoted BY Filed should be at least 3 characters")
        elif not quoted_by:
            error.append("This field must be filled out")  # END OF QUOTED BY VALIDATION

        if len(newMsg) < 10:
            error.append("Minimum 10 characters")  # END OF MESSAGE VALIDATION

        if len(error) > 0:
            return [False, error]
        if len(error) > 0:
            return [False, error]
        else:
            newQuote = Quotes.QuoteManager.create(message=newMsg, quoted_by=quoted_by, created_by=user.username,
                                                  created_at=now, updated_at=now)
            return [True]


    def validquoted_by(self, quoted_by):
        if len(quoted_by) < 3:
            return True
        else:
            return False

    def validmessage(self, newMsg):
        if len(newMsg) < 10:
            return True
        else:
            return False

class Users(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    email = models.CharField(max_length=60, blank=True)
    password = models.CharField(max_length=45)
    date = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    UserManager = UserManager()


class Quotes(models.Model):
    message = models.CharField(max_length=45)
    quoted_by = models.CharField(max_length=30, blank=True)
    owned_by = models.ManyToManyField(Users, blank=True)
    created_by = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    QuoteManager = QuoteManager()
