from django.shortcuts import render




def landing(request):
  return render(request, 'landing.html')


def user_auth(request):
  return render(request, 'user_auth.html')


def profile(request):
  return render(request, 'profile_new_one.html')


def edit_profile(request):
  return render(request, 'edit_profile.html')


def main(request):
  return render(request, 'main_new.html')


def browse(request):
  return render(request, 'browse_one.html')


def faq(request):
  return render(request, 'faq.html')


def feed(request):
  return render(request, 'feed.html')


def post_feed(request):
  return render(request, 'post_feed.html')




