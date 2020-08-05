from plaid_integration.Item.models import Account
from plaid_integration.Item.models import Item
from plaid_integration.celery import app
from plaid_integration.plaid.plaid import plaid_helper


@app.task
def get_or_create_item(user_id, public_token):
    item_data = plaid_helper.get_or_create_item(public_token)
    item = Item.objects.create(user_id=user_id,
                               access_token=item_data['acccess_token'],
                               item_id=item_data['item_id'])
    accounts = plaid_helper.get_accounts(item_data['access_token'])
    for account in accounts:
        Account.objects.get_or_create(account_id=account['account_id'],
                                      item_id=item.id,
                                      name=account['name'])
