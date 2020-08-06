How to use:
1. clone the project.
2. Import in django, set interpreter, virtual env, install requirements according to pycharm's suggestions.
3. if you dont want to do (2): create virtual env using virtualenv, activate it, run: pip istall - requirements.txt
4. If you want to test from scratch, remove db.sqlite3 file and run this command:
   python manage.py migrate
6. setup rabbitmq at port of your choice, change BROKER_URL in settings file acc. to the port.
   by default it will run at 56720.
5. Run app using pycharm django server config/command:
   python manage.py runserver.
6. run celery worker using command: celery -A plaid_integration worker --loglevel=info
7. test APIs using the postman collection provided.
8. authentication is token based. use the key returned in login/signup API in authentication token for
   product APIs: get_transactions, get_accounts, get_or_create_item(to exchange public_token to access_token)
9. public token can be fetched from the quickstart app here:https://plaid.com/docs/quickstart/. (clone,run flask app, login using user_good username and pass_good pwd, inspect element, get public_token from set_access_token API)
