# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from plaid_integration.Item.models import Account, Transaction
from plaid_integration.Item.tasks import get_or_create_item, process_transaction_updates


class ItemViewSet(GenericViewSet):
    def get_permissions(self):
        permissions = super().get_permissions()
        if self.action in ['get_or_create_item', 'get_accounts', 'get_transactions']:
            permissions.append(IsAuthenticated())
        return permissions

    @action(detail=False, methods=['POST'])
    def get_or_create_item(self, request, *args, **kwargs):
        user_id = request.user.id
        public_token = request.data.get('public_token')
        if not public_token:
            return Response(status=HTTP_400_BAD_REQUEST)
        print('Publishing task : {}'.format(get_or_create_item))
        get_or_create_item.delay(user_id, public_token)
        return Response(status=HTTP_202_ACCEPTED)

    @action(detail=False, methods=['GET'])
    def get_accounts(self, request, *args, **kwargs):
        accounts = Account.objects.filter(item__user_id=request.user.id).values('account_id', 'balances',
                                                                                'item__item_id', 'name', 'mask',
                                                                                'official_name', 'type', 'subtype')
        return Response(status=HTTP_200_OK,
                        data={'accounts': accounts})

    @action(detail=False, methods=['GET'])
    def get_transactions(self, request, *args, **kwargs):
        user_id = request.user.id
        transactions = Transaction.objects.filter(account__item__user_id=user_id, is_deleted=False).values('account_id',
                                                                                                           'account_owner',
                                                                                                           'amount',
                                                                                                           'authorized_date',
                                                                                                           'category',
                                                                                                           'date',
                                                                                                           'iso_currency_code',
                                                                                                           'location',
                                                                                                           'merchant_name',
                                                                                                           'name',
                                                                                                           'payment_channel',
                                                                                                           'payment_meta',
                                                                                                           'pending',
                                                                                                           'pending_transaction_id',
                                                                                                           'transaction_code',
                                                                                                           'transaction_id',
                                                                                                           'transaction_type',
                                                                                                           'unofficial_currency_code',
                                                                                                           'is_deleted')
        return Response(status=HTTP_200_OK, data={'transactions': transactions})

    @action(detail=False, methods=['POST'])
    def webhook(self, request, *args, **kwargs):
        webhook_data = request.data
        process_transaction_updates.delay(webhook_data)
        return Response(status=HTTP_202_ACCEPTED)
