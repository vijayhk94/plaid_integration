# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CharField, ForeignKey, DateTimeField, JSONField, FloatField, DateField, NullBooleanField, BooleanField


class Item(models.Model):
    item_id = CharField(unique=True, max_length=50)
    user = ForeignKey(get_user_model(), on_delete=models.CASCADE)
    access_token = CharField(unique=True, max_length=100)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now_add=True)
    institute_name = CharField(max_length=50, null=True, blank=True)
    available_products = JSONField(null=True, blank=True)
    billed_products = JSONField(null=True, blank=True)


class Account(models.Model):
    account_id = CharField(max_length=50)
    balances = JSONField(null=True, blank=True)
    item = ForeignKey(Item, on_delete=models.CASCADE)
    name = CharField(max_length=50, null=True, blank=True)
    mask = CharField(max_length=10, null=True, blank=True)
    official_name = CharField(max_length=100, null=True, blank=True)
    type = CharField(max_length=15, null=True, blank=True)
    subtype = CharField(max_length=15, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    account = ForeignKey(Account, on_delete=models.CASCADE)
    account_owner = CharField(max_length=50, null=True, blank=True)
    amount = FloatField()
    authorized_date = DateField(null=True, blank=True)
    category = JSONField(null=True, blank=True)
    date = DateField(null=True, blank=True)
    iso_currency_code = CharField(max_length=15, null=True, blank=True)
    location = JSONField(null=True, blank=True)
    merchant_name = CharField(max_length=50, null=True, blank=True)
    name = CharField(max_length=50, null=True, blank=True)
    payment_channel = CharField(max_length=50, null=True, blank=True)
    payment_meta = JSONField(null=True, blank=True)
    pending = NullBooleanField()
    pending_transaction_id = CharField(max_length=100, null=True, blank=True)
    transaction_code = CharField(max_length=100, null=True, blank=True)
    transaction_id = CharField(max_length=100, null=True, blank=True)
    transaction_type = CharField(max_length=25, null=True, blank=True)
    unofficial_currency_code = CharField(max_length=15, null=True, blank=True)
    is_deleted = BooleanField(default=False)

# Create your models here.
