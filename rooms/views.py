from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_str, force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings


from .models import User, UserProfile, UserProfileImage, UserMajors, UserCourses
# from .forms import ImageForm
from . import utils






def activate(request, uidb64, token):
  User = get_user_model()
  try:
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None

  if user is not None and utils.TokenGenerator().check_token(user, token):
    user.is_active = True
    user.save()
    return redirect('email_validation_success.html')
  else:
    # return HttpResponse('Activation link is invalid!')
    return render(request, 'email_validation_error.html')



def validate_email(request):
  return render(request, 'email_validation_success.html')  



# TODO: only available if user is not authenticated; else, send to our 'default-page' (main-page?)
def landing(request):
  if request.method == 'POST':

    if 'login_form' in request.POST:
      user_email = request.POST['school_email']
      user_password = request.POST['password']
      user_obj = authenticate(username=user_email, password=user_password)
      if user_obj is not None:
        login(request, user_obj)
        return redirect("profile")
      else:
        form_data = {'email': user_email}
        return render(request, 'landing.html', {
          'view_login_form': True, 'form_data': form_data, 'error_message': 'invalid email/password...', 'form_error': True})


    elif 'signup_form' in request.POST: # TODO: send verification email and set created user to inactive on initial save until email-verif.
      user_email = request.POST['school_email']
      user_first_name = request.POST['first_name']
      user_last_name = request.POST['last_name']
      user_password = request.POST['password']

      # TODO: need to send verification email (set is_active=False; once verified, set is_active=True; <-- critical check)
      valid_email = utils.verify_school_email(user_email)
      valid_password, password_msg = utils.validate_password(user_password)

      if valid_email and valid_password:
        user_objects = User.objects.filter(email=user_email)
        # if len(user_objects) == 0:
        if len(user_objects) == 0:
          # TODO: set new user as in-active; email must be verified before access given 
          new_user_obj = User.objects.create_user(
            email=user_email, 
            password=user_password,
            is_active=False
          )
          new_user_obj.first_name = user_first_name
          new_user_obj.last_name = user_last_name
          new_user_obj.save()

          current_site = get_current_site(request)

          message = render_to_string('email_template.html', {
            'user': new_user_obj,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(new_user_obj.pk)),
            'token': utils.TokenGenerator().make_token(new_user_obj),
          })
        
          send_mail(
            subject='UofT Room Verification Email',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['duggalr42@gmail.com']
          )

          # user_authenticated = authenticate(username=user_email, password=user_password)
          # login(request, user_authenticated)
          # return redirect('landing')
          return render(request, 'landing.html', {'form_error': False, 'signup_success': True})

        else:
          existing_user_obj = user_objects[0]
          if existing_user_obj.is_active:
            form_data = {'email': user_email, 'first_name': user_first_name, 'last_name': user_last_name}
            return render(request, 'landing.html', {'form_data': form_data, 'error_message': 'user already exists...', 'form_error': True})
          else:
            current_site = get_current_site(request)

            message = render_to_string('email_template.html', {
              'user': existing_user_obj,
              'domain': current_site.domain,
              'uid': urlsafe_base64_encode(force_bytes(existing_user_obj.pk)),
              'token': utils.TokenGenerator().make_token(existing_user_obj),
            })

            send_mail(
              subject='UofT Room Verification Email',
              message=message,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=['duggalr42@gmail.com']
            )
            
            return render(request, 'landing.html', {'form_error': False, 'signup_success': True})
            
          # # TODO: confirm the user's email is verified; if so, login the user; else, pass error with existing user & wrong password          
          # form_data = {'email': user_email, 'first_name': user_first_name, 'last_name': user_last_name}
          # return render(request, 'landing.html', {'form_data': form_data, 'error_message': 'user already exists...', 'form_error': True})

      else:

        if not valid_email:
          form_data = {'email': user_email, 'first_name': user_first_name, 'last_name': user_last_name}
          return render(request, 'landing.html', {
            'form_data': form_data, 'error_message': 'not a valid uoft email...', 'form_error': True})

        elif not valid_password:
          form_data = {'email': user_email, 'first_name': user_first_name, 'last_name': user_last_name}
          return render(request, 'landing.html', {
            'form_data': form_data, 'error_message': 'password must be >7 letters and have at least 1 character and 1 number.', 'form_error': True})


  return render(request, 'landing.html', {'view_login_form': False})




# # TODO: implement exact same as above on this page...
# def user_auth(request):
#   return render(request, 'user_auth.html')


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
    return render(request, 'profile_new_three.html', {'user_info': user_info})

  else:  # TODO: redirect to landing
    print(request)
    return redirect('landing')



def edit_profile(request):
  # TODO: check if user authenticatd/active and pass the name of user from initial signup to edit-profile
  if request.user.is_authenticated and request.user.is_active:  # TODO: is_active is crucial; ensure it is adjusted appror. above

    uoft_programs_fp = '/Users/rahul/Documents/main/projects/personal_learning_projects/uoftroom/final_programs_list.txt'
    f = open(uoft_programs_fp, 'r')
    uoft_programs = f.readlines()
    uoft_programs = [line.replace('\n', '').strip() for line in uoft_programs]

    uoft_courses_fp = '/Users/rahul/Documents/main/projects/personal_learning_projects/uoftroom/uoft_all_courses.txt'
    f = open(uoft_courses_fp, 'r')
    uoft_courses = f.readlines()
    uoft_courses = [line.replace('\n', '').strip() for line in uoft_courses]

    if request.method == 'POST':
      print('request-post:', request.POST)

      gender = request.POST['gender']
      instagram_id = request.POST['instagram-id']
      snapchat_id = request.POST['snapchat-id']
      spotify_id = request.POST['spotify-id']
      current_school_status = request.POST['current_status']
      user_campus = request.POST['campus']
      
      user_college = request.POST['user_college']
      user_year = request.POST['user_year']
      if user_year == '':
        user_year = None
      living_on_res = request.POST['living_on_res']
      if living_on_res == '':
        living_on_res = None
      user_job = request.POST['user_job']
      # user_jobs = request.POST.getlist('user_job')
      user_location = request.POST['user_location']
      current_relationship_status = request.POST['current_relationship_status']
      user_description = request.POST['user_description']
      user_interests = request.POST['user_interest']

      user_major_list = request.POST.getlist('user_major')
      user_course_list = request.POST.getlist('courses')
      
      up_objects = UserProfile.objects.filter(user_obj=request.user)
      if len(up_objects) > 0:
        up_obj = up_objects[0]
        up_obj.instagram_id = instagram_id
        up_obj.snapchat_id = snapchat_id
        up_obj.spotify_url = spotify_id
        up_obj.gender = gender
        up_obj.current_school_status = current_school_status
        up_obj.current_school_campus = user_campus
        up_obj.current_school_year = user_year
        up_obj.current_college = user_college
        up_obj.living_on_res = living_on_res
        up_obj.user_location = user_location
        up_obj.user_relationship_status = current_relationship_status
        up_obj.job_companies = user_job
        up_obj.user_description = user_description
        up_obj.user_interests = user_interests
        up_obj.save()

      else: 
        up_obj = UserProfile.objects.create(
          user_obj=request.user,
          instagram_id=instagram_id, 
          snapchat_id=snapchat_id,
          spotify_url=spotify_id,
          gender=gender, 
          current_school_status=current_school_status,
          current_school_campus=user_campus,
          current_school_year=user_year,
          current_college=user_college,
          living_on_res=living_on_res,
          user_location=user_location,
          user_relationship_status=current_relationship_status,
          job_companies=user_job,
          user_description=user_description,
          user_interests=user_interests
        )
        up_obj.save()

      um_objects = UserMajors.objects.filter(user_profile_obj = up_obj)
      # if len(um_objects) > 0:
      UserMajors.objects.filter(user_profile_obj = up_obj).delete()  # recreate it

      for user_major in user_major_list:
        um = UserMajors.objects.create(
          user_profile_obj = up_obj,
          major = user_major
        )
        um.save()
      
      uc_objects = UserCourses.objects.filter(user_profile_obj = up_obj)
      # if len(uc_objects) > 0:
      UserCourses.objects.filter(user_profile_obj = up_obj).delete() 

      for user_course in user_course_list:
        uc = UserCourses.objects.create(
          user_profile_obj = up_obj,
          course = user_course
        )
        uc.save()

      profile_images = request.FILES.getlist('profile_image')
      UserProfileImage.objects.filter(user_profile_obj = up_obj).delete()
      for fn in profile_images:
        upi = UserProfileImage(
          user_profile_obj = up_obj,
          profile_image=fn
        )
        upi.save()


    user_first_name = request.user.first_name
    user_last_name = request.user.last_name
    up_objects = UserProfile.objects.filter(user_obj=request.user)
    up_obj = None
    course_str = ''
    user_major_str = ''
    if len(up_objects) > 0: 
      up_obj = up_objects[0]
      user_courses = UserCourses.objects.filter(user_profile_obj=up_obj)
      course_str = ','.join([obj.course for obj in user_courses])
      user_majors = UserMajors.objects.filter(user_profile_obj=up_obj)
      user_major_str = ','.join([obj.major for obj in user_majors])

    user_info = {
      'first_name': user_first_name, 
      'last_name': user_last_name,
      'up_obj': up_obj,
      'user_course_str': course_str,
      'user_major_str': user_major_str
    }
    return render(request, 'edit_profile_one.html', {
      'user_info': user_info, 'programs': uoft_programs, 'courses': uoft_courses,
    })

  else: 
    return redirect('landing')
  


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




