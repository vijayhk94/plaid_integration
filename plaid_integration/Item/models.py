# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CharField, ForeignKey, DateTimeField


class Item(models.Model):
    item_id = CharField(unique=True, max_length=50)
    user = ForeignKey(get_user_model(), on_delete=models.CASCADE)
    access_token = CharField(unique=True, max_length=100)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now_add=True)


class Account(models.Model):
    account_id = CharField(max_length=50)
    item = ForeignKey(Item, on_delete=models.CASCADE)
    name = CharField(max_length=50)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now_add=True)

# Create your models here.
