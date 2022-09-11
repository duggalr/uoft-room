from django.urls import path

from . import views


urlpatterns = [
  path('', views.landing, name='landing'),
  path('edit_profile', views.edit_profile, name='edit_profile'),

  path('main', views.main, name='main'),
  path('profile', views.profile, name='profile'),
  path('browse', views.browse, name='browse'),
  path('faq', views.faq, name='faq'),

  path('feed', views.feed, name='feed'),
  path('post_feed', views.post_feed, name='post_feed'),

  path('user-verification/<uidb64>/<token>', views.activate, name='user_verification'),

  # path('auth', views.user_auth, name='user_auth'),

  path('validate_email', views.validate_email, name='validate_email'),

  path('logout', views.logout_view, name='logout'),

]





