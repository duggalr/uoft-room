from django.urls import path

from . import views


urlpatterns = [
  path('', views.landing, name='landing'),
  path('main', views.main, name='main'),
  path('profile', views.profile, name='profile'),
  path('browse', views.browse, name='browse'),
  path('faq', views.faq, name='faq'),
]





