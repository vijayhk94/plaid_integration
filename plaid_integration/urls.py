"""plaid_integration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from plaid_integration.Item.views import ItemViewSet

router = SimpleRouter()
router.register(r'item', ItemViewSet, basename='item')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('rest_auth.urls')),
    path('accounts/signup/', include('rest_auth.registration.urls')),
    path('', include(router.urls))]
