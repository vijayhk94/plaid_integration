from plaid_integration.Item.models import Account
from plaid_integration.Item.models import Item
from plaid_integration.celery import app
from plaid_integration.plaid.plaid import plaid_helper


@app.task
def get_or_create_item(user_id, public_token):
    item_data = plaid_helper.get_or_create_item(public_token)
    print(item_data)
    item_dict = plaid_helper.get_item(item_data['access_token'])
    print(item_dict)
    institute_name = plaid_helper.get_institute_name(item_dict['institution_id'])
    if Item.objects.filter(item_id=item_data['id']).exists():
        item = Item.objects.get(item_id=item_data['id'])
    else:
        item = Item.objects.create(user_id=user_id,
                                   access_token=item_data['access_token'],
                                   item_id=item_data['id'],
                                   available_products=item_dict['available_products'],
                                   billed_products=item_dict['billed_products'],
                                   institute_name=institute_name
                                   )
    accounts = plaid_helper.get_accounts(item_data['access_token'])
    print(accounts)
    for account in accounts:
        Account.objects.get_or_create(account_id=account['account_id'],
                                      item_id=item.id,
                                      name=account['name'],
                                      balances=account['balances'],
                                      official_name=account['official_name'],
                                      mask=account['mask'],
                                      type=account['type'],
                                      subtype=account['subtype'])
