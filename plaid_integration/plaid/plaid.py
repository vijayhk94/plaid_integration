import plaid
from django.conf import settings


class Plaid():
    def __init__(self):
        self.client = plaid.Client(client_id=settings.PLAID_CLIENT_ID, secret=settings.PLAID_SECRET,
                                   environment=settings.PLAID_ENV)

    def get_or_create_item(self, public_token):
        item = self.client.Item.public_token.exchange(public_token)
        return {'access_token': item.get('access_token'), 'id': item.get('item_id')}

    def get_accounts(self, access_token):
        return self.client.Accounts.get(access_token).get('accounts', [])

    def get_item(self, access_token):
        return self.client.Item.get(access_token).get('item', {})

    def get_institute_name(self, id):
        return self.client.Institutions.get_by_id(id)['institution']['name']

    def get_transactions(self, access_token, start_time, end_time):
        response = self.client.Transactions.get(access_token, start_date=start_time, end_date=end_time)
        transactions = response['transactions']

        # the transactions in the response are paginated, so make multiple calls while increasing the offset to
        # retrieve all transactions
        while len(transactions) < response['total_transactions']:
            response = self.client.Transactions.get(access_token, start_date=start_time, end_date=end_time,
                                                    offset=len(transactions)
                                                    )
            transactions.extend(response['transactions'])
        return transactions

    # def get_transactions(self, ):


plaid_helper = Plaid()
