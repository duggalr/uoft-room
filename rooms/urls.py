from django.urls import path

from . import views


urlpatterns = [
  path('', views.landing, name='landing'),
  path('auth', views.user_auth, name='user_auth'),
  path('edit_profile', views.edit_profile, name='edit_profile'),

  path('main', views.main, name='main'),
  path('profile', views.profile, name='profile'),
  path('browse', views.browse, name='browse'),
  path('faq', views.faq, name='faq'),

  path('feed', views.feed, name='feed'),
]





