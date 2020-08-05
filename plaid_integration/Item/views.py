# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from plaid_integration.Item.models import Account
from plaid_integration.Item.tasks import get_or_create_item


class ItemViewSet(GenericViewSet):
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
        accounts = Account.objects.filter(item__user_id=request.user.id) \
            .values('account_id', 'name')
        return Response(status=HTTP_200_OK,
                        data={'accounts': accounts})
