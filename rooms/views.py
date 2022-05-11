from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .models import User
from . import utils



# TODO: only available if user is not authenticated; else, send to our 'default-page'
def landing(request):
  if request.method == 'POST':
    print(request.POST)
    user_email = request.POST['school_email']
    user_first_name = request.POST['first_name']
    user_last_name = request.POST['last_name']
    user_password = request.POST['password']
    # TODO: need to send verification email (set is_active=False; once verified, set is_active=True; <-- critical check)
    valid_email = utils.verify_school_email(user_email)
    if valid_email:
      user_objects = User.objects.filter(email=user_email)
      if len(user_objects) == 0:
        new_user_obj = User.objects.create_user(user_email, user_password)
        new_user_obj.first_name = user_first_name
        new_user_obj.last_name = user_last_name
        new_user_obj.save()

        user_authenticated = authenticate(username=user_email, password=user_password)
        login(request, user_authenticated)
        return redirect('profile')
      else:
        form_data = {'email': user_email, 'first_name': user_first_name, 'last_name': user_last_name}
        return render(request, 'landing.html', {'form_data': form_data, 'error_message': 'user already exists...', 'form_error': True})
    else:
      form_data = {'email': user_email, 'first_name': user_first_name, 'last_name': user_last_name}
      return render(request, 'landing.html', {
        'form_data': form_data, 'error_message': 'not a valid uoft email...', 'form_error': True})

  return render(request, 'landing.html')


# TODO: implement exact same as above on this page...
def user_auth(request):
  return render(request, 'user_auth.html')


def profile(request):
  if request.user.is_authenticated and request.user.is_active:  # TODO: is_active is crucial; ensure it is adjusted appror. above
    print('user:', request.user)
    user_first_name = request.user.first_name
    user_last_name = request.user.last_name
    user_info = {
      'first_name': user_first_name, 
      'last_name': user_last_name
    }
    # TODO: need profile data
    return render(request, 'profile_new_one.html', {'user_info': user_info})

  else:  # TODO: redirect to landing
    print(request)

  return render(request, 'profile_new_one.html')


def edit_profile(request):
  uoft_programs_fp = '/Users/rahul/Documents/main/projects/personal_learning_projects/uoftroom/final_programs_list.txt'
  f = open(uoft_programs_fp, 'r')
  lines = f.readlines()
  lines = [line.replace('\n', '').strip() for line in lines]
  return render(request, 'edit_profile.html', {'programs': lines})


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




