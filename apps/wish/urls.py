from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^home$', views.home),
    url(r'^login', views.loginUser),
    url(r'^logout', views.logout),
    url(r'^register$', views.registerUser),
    url(r'^addQuote$', views.addQuote),
    url(r'^singleQuote/(?P<created_by>\w+)$', views.singleQuote),
    url(r'^addremove$', views.addremove)
]