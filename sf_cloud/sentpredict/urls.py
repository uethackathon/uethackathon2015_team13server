from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.predict, name='predict'),
    url(r'^', views.predict, name='predict')
]