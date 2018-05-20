from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^books/$', views.books, name="home"),
    url(r'^books/add/$', views.add, name="add"),
    url(r'^books/add/new/$', views.new_book, name="new_book"),
    url(r'^books/(?P<id>\d+)/$', views.show_book, name="show_book"),
    url(r'^books/(?P<id>\d+)/new_review/$', views.new_review, name="new_review"),
    url(r'^users/new$', views.new_user, name="new_user"),
    url(r'^users/(?P<id>\d+)/$', views.show_user, name="show_user"),
    url(r'^users/login$', views.login, name="login"),
    url(r'^users/logout$', views.logout, name="logout"),
    url(r'^users/reviews/(?P<id>\d+)/$', views.delete_review, name="delete"),
]
