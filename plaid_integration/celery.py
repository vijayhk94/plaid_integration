from celery import Celery
from django.conf import settings

app = Celery('plaid_integration', broker=settings.BROKER_URL)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
