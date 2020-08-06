from datetime import date

from plaid_integration.Item.models import Account
from plaid_integration.Item.models import Item, Transaction
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


@app.task()
def process_transaction_updates(transactions_data):
    if not transactions_data.get('webhook_type'):
        print('webhook_type not present in transactions_data. exiting')
        return
    if transactions_data.pop('webhook_type', '') != 'TRANSACTIONS':
        print('This is not a transactions webhook. exiting.')
        return
    item_id = transactions_data.get('item_id')
    if not Item.objects.filter(item_id=item_id).exists():
        print('item for transaction not found. exiting')
        return
    webhook_code = transactions_data.get('webhook_code')
    if webhook_code == 'TRANSACTIONS_REMOVED':
        Transaction.objects.filter(transaction_id__in=transactions_data.get('removed_transactions', [])).update(
            is_deleted=True)
    elif webhook_code in ['INITIAL_UPDATE', 'HISTORICAL_UPDATE', 'DEFAULT_UPDATE', 'TRANSACTIONS_REMOVED']:
        item_id = transactions_data.get('item_id')
        try:
            item = Item.objects.get(item_id=item_id)
        except Item.DoesNotExist as exc:
            print('did not find item with id: {}.exiting'.format(item_id))
            return
        start_time = '2000-01-01'
        end_time = date.today().strftime('%Y-%m-%d')
        transactions = plaid_helper.get_transactions(item.access_token, start_time, end_time)
        for transaction in transactions:
            account_id = Account.objects.get(account_id=transaction.get('account_id')).id
            Transaction.objects.get_or_create(account_id=account_id,
                                              account_owner=transaction.get('account_owner'),
                                              amount=transaction.get('amount'),
                                              authorized_date=transaction.get('authorized_date'),
                                              category=transaction.get('category'),
                                              date=transaction.get('date'),
                                              iso_currency_code=transaction.get('iso_currency_code'),
                                              location=transaction.get('location'),
                                              merchant_name=transaction.get('merchant_name'),
                                              name=transaction.get('name'),
                                              payment_channel=transaction.get('payment_channel'),
                                              payment_meta=transaction.get('payment_meta'),
                                              pending=transaction.get('pending'),
                                              pending_transaction_id=transaction.get('pending_transaction_id'),
                                              transaction_code=transaction.get('transaction_code'),
                                              transaction_id=transaction.get('transaction_id'),
                                              transaction_type=transaction.get('transaction_type'),
                                              unofficial_currency_code=transaction.get('unofficial_currency_code'),
                                              is_deleted=False)
