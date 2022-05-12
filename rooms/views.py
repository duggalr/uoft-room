from cgitb import reset
from distutils.command.upload import upload
import re
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .models import User, UserProfileImage
# from .forms import ImageForm
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
  # TODO: check if user authenticatd/active and pass the name of user from initial signup to edit-profile

  uoft_programs_fp = '/Users/rahul/Documents/main/projects/personal_learning_projects/uoftroom/final_programs_list.txt'
  f = open(uoft_programs_fp, 'r')
  uoft_programs = f.readlines()
  uoft_programs = [line.replace('\n', '').strip() for line in uoft_programs]

  uoft_courses_fp = '/Users/rahul/Documents/main/projects/personal_learning_projects/uoftroom/uoft_all_courses.txt'
  f = open(uoft_courses_fp, 'r')
  uoft_courses = f.readlines()
  uoft_courses = [line.replace('\n', '').strip() for line in uoft_courses]


  if request.method == 'POST':
    print(request.FILES)
    profile_images = request.FILES.getlist('profile_image')
    
    # for fn in profile_images:
    #   b = UserProfileImage(profile_image=fn)
    #   b.save()

    # TODO: UI of form, save form, redirect, edit-form, and go from there



    # print(request.POST)
    # user_majors = request.POST.getlist('user_major')
    # user_courses = request.POST.getlist('user_courses')

    # files_list = request.FILES.getlist('profile_image')
    # gender = request.POST['gender']
    # instagram_id = request.POST['instagram-id']
    # snapchat_id = request.POST['snapchat-id']
    # spotify_id = request.POST['spotify-id']
    # current_school_status = request.POST['current_status']
    # user_campus = request.POST['campus']
    # user_year = request.POST['user_year']
    # user_college = request.POST['user_college']
    # living_on_res = request.POST['living_on_res']
    # user_major = request.POST.getlist('user_major')
    # user_courses = request.POST.getlist('courses')
    # user_jobs = request.POST.getlist('user_job')
    # user_location = request.POST['user_location']
    # current_relationship_status = request.POST['current_relationship_status']
    # pizza_topping = request.POST['pizza_topping']


    # for fn in files_list:
    #   b = TestingImage(image_file=request.FILES['files'], person_name=request.POST['person_name'])
    #   b.save()

    
  #   image_file = request.FILES.popitem()[0]
  #   b = TestingImage(image_file=image_file)
  #   b.save()

# _, file = request.FILES.popitem()  # get first element of the uploaded files

#         file = file[0]  # get the file from MultiValueDict

#         file_model.file = file
#         file_model.save()

    # print(request.body)
    # print(request.POST)
    # print(request.FILES)
    # uploaded_images = request.FILES['profile_image']
    # print(uploaded_images)
      # fss = FileSystemStorage()
    # file = fss.save(upload.name, upload)
    # file_url = fss.url(file)

  # return render(request, 'edit_profile.html', {'programs': lines})
  return render(request, 'edit_profile_one.html', {'programs': uoft_programs, 'courses': uoft_courses})


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




