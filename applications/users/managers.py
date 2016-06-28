# -*- coding: utf-8 -*-
# __author__ = xutao

from __future__ import division, unicode_literals, print_function
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, id=None, email=None, password="123456"):
        user = self.model()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id=None, email=None, password="admin"):
        user = self.model()
        user.set_password(password)
        user.email = email
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user