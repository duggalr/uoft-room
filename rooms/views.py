from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
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



def create_new_user(user_email, user_password):
  new_user_obj = User.objects.create_user(
    email=user_email, 
    password=user_password,
    is_active=True  # TODO: setting this is active for now; ensure this is set to inactive when implementing email-send**
  )
  new_user_obj.save()

  # TODO: 
    # creating user-profile here but move to email-activation-function 
    # **only create this when user is activated, never before
  
  up_obj = UserProfile.objects.create(
    user_obj = new_user_obj
  )
  up_obj.save()

  return new_user_obj



# TODO: only available if user is not authenticated; else, send to our 'default-page' (main-page?)
def landing(request):

  if request.method == 'POST':
    user_email = request.POST['school_email']
    user_password = request.POST['password']

    user_objects = User.objects.filter(email=user_email)
    if len(user_objects) == 0: # new-user
      valid_email = utils.verify_school_email(user_email)
      valid_password, password_msg = utils.validate_password(user_password)


      if valid_email and valid_password:
        new_user_obj = create_new_user(user_email, user_password)

        # current_site = get_current_site(request)
        # message = render_to_string('email_template.html', {
        #   'user': new_user_obj,
        #   'domain': current_site.domain,
        #   'uid': urlsafe_base64_encode(force_bytes(new_user_obj.pk)),
        #   'token': utils.TokenGenerator().make_token(new_user_obj),
        # })

        # TODO: what if email fails to send? <-- important to catch exceptions here and inform user**
        # send_mail(
        #   subject='UofT Room Verification Email',
        #   message=message,
        #   from_email=settings.EMAIL_HOST_USER,
        #   recipient_list=['duggalr42@gmail.com']
        # )

        return render(request, 'landing.html', {'form_error': False, 'signup_success': True})

      else:
        if not valid_email:
          form_data = {'email': user_email}
          return render(request, 'landing.html', {
            'form_data': form_data, 
            'error_message': 'not a valid uoft email...', 
            'form_error': True
          })

        elif not valid_password:
          form_data = {'email': user_email}
          return render(request, 'landing.html', {
            'form_data': form_data, 
            'error_message': 'password must be >7 letters and have at least 1 character and 1 number.', 
            'form_error': True
          })

    else: # authenticate or deal with inactive-user
      user_obj = authenticate(username=user_email, password=user_password)

      if user_obj is not None: # valid user; login and redirect
        login(request, user_obj)
        return redirect("browse")

      else: # check case of inactive/active
        existing_user_obj = user_objects[0]  # really should never be >1 ?
        if existing_user_obj.is_active:  # user is active; invalid login attempt
          form_data = {'email': user_email}
          return render(request, 'landing.html', {'form_data': form_data, 'error_message': 'invalid email/password...', 'form_error': True})
        
        else: # user is inactive; re-create user and send activation email again
          User.objects.filter(email=user_email).delete() # delete previous user and create new one (possibly new password)

          valid_password, password_msg = utils.validate_password(user_password)

          if valid_password:
            new_user_obj = create_new_user(user_email, user_password)

            # current_site = get_current_site(request)
            # message = render_to_string('email_template.html', {
            #   'user': new_user_obj,
            #   'domain': current_site.domain,
            #   'uid': urlsafe_base64_encode(force_bytes(new_user_obj.pk)),
            #   'token': utils.TokenGenerator().make_token(new_user_obj),
            # })

            # # TODO: what if email fails to send? <-- important to catch exceptions here and inform user**
            # send_mail(
            #   subject='UofT Room Verification Email',
            #   message=message,
            #   from_email=settings.EMAIL_HOST_USER,
            #   recipient_list=['duggalr42@gmail.com']
            # )
            return render(request, 'landing.html', {'form_error': False, 'signup_success': True})

          else:
            form_data = {'email': user_email}
            return render(request, 'landing.html', {
              'form_data': form_data, 
              'error_message': 'password must be >7 letters and have at least 1 character and 1 number.', 
              'form_error': True
            })

  return render(request, 'landing.html', {'view_login_form': False})
    


# TODO: add login_required and appr. redirect
def profile(request, profile_id):
  if request.user.is_authenticated and request.user.is_active:  # TODO: is_active is crucial; ensure it is adjusted appror. above
    print('user:', request.user)

    # user_profile_obj = UserProfile.objects.get(user_obj=request.user)
    user_profile_obj = get_object_or_404(UserProfile, id=profile_id)
    user_courses = UserCourses.objects.filter(user_profile_obj=user_profile_obj)

    same_user = False
    if user_profile_obj.user_obj == request.user:
      same_user = True
    

    # TODO: ensure user_majors is correct
    # user_majors = UserMajors.objects.get(user_profile_obj=user_profile_obj)  # should be string of all majors for user
    # user_majors_list = ', '.join([st for st in user_majors.major.split(',')])

    user_profile_images = UserProfileImage.objects.filter(user_profile_obj=user_profile_obj)

    user_image_list = [{'idx': i+1, 'profile_image': user_profile_images[i]} for i in range(len(user_profile_images))]
    
    return render(request, 'profile_new_three.html', {
      'same_user': same_user,
      'user_profile_images': user_image_list,
      'user_profile_obj': user_profile_obj,
      'user_courses': user_courses,
      # 'user_majors': user_majors_list
    })

    # user_first_name = request.user.first_name
    # user_last_name = request.user.last_name
    # user_info = {
    #   'first_name': user_first_name, 
    #   'last_name': user_last_name
    # }

    # TODO: 
      # fetch all the profile data and show on profile-page; go from there
      # add the edit button to top of profile page 
      # remove the 'eye' on top (just have the emoji on the profile-view-section)
      # test the image functionality (uploading/removing-images, etc)

    # user_profile_obj = UserProfile.objects.get(user_obj=request.user)
    # return render(request, 'profile_new_three.html', {'user_info': user_info})
    # return render(request, 'profile_new_three.html', {'user_profile_obj': user_profile_obj})

  else:  # TODO: redirect to landing
    return redirect('landing')



# TODO: 
  # add login-required here and ensure user is active (valid email address)
def edit_profile(request):
  if request.user.is_authenticated and request.user.is_active:

    uoft_programs_fp = 'final_programs_list.txt'
    f = open(uoft_programs_fp, 'r')
    uoft_programs = f.readlines()
    uoft_programs = [line.replace('\n', '').strip() for line in uoft_programs]

    uoft_courses_fp = 'uoft_all_courses.txt'
    f = open(uoft_courses_fp, 'r')
    uoft_courses = f.readlines()
    uoft_courses = [line.replace('\n', '').strip() for line in uoft_courses]

    if request.method == 'POST':
      print('request-post:', request.POST)

      first_name = request.POST['first-name']
      last_name = request.POST['last-name']
      gender = request.POST['gender']
      instagram_id = request.POST['instagram-id']
      snapchat_id = request.POST['snapchat-id']
      spotify_id = request.POST['spotify-id']
      current_school_status = request.POST['current_status']
      user_campus = request.POST['campus']
      
      user_college = request.POST['user_college']
      user_year = request.POST['user_year']
      
      # print('ue:', user_year)
      # if user_year == 'None':
      #   print('ue-two:', user_year)
      #   user_year = None

      living_on_res = request.POST['living_on_res']
 
      user_job = request.POST['user_job']
      # user_jobs = request.POST.getlist('user_job')

      user_location = request.POST['user_location']
      current_relationship_status = request.POST['current_relationship_status']
      user_description = request.POST['user_description']
      user_interests = request.POST['user_interest']

      user_major_list = request.POST.getlist('user_major')
      user_course_list = request.POST.getlist('courses')
      profile_images = request.FILES.getlist('profile_image')
      
      up_objects = UserProfile.objects.get(user_obj=request.user)
      # if len(up_objects) > 0:
        # up_obj = up_objects[0]
        
      if request.POST['first-name'] is not None:
        up_obj.first_name = request.POST['first-name']
      
      if request.POST['last-name'] is not None:
        up_obj.last_name = request.POST['last-name']

      if request.POST['gender'] is not None:
        up_obj.gender = request.POST['gender']

      if request.POST['instagram-id'] is not None:
        up_obj.instagram_id = request.POST['instagram-id']
      
      if request.POST['snapchat-id'] is not None:
        up_obj.snapchat_id = request.POST['snapchat-id']

      if request.POST['spotify-id'] is not None:
        up_obj.spotify_url = request.POST['spotify-id']

      if request.POST['current_status'] is not None:
        up_obj.current_school_status = request.POST['current_status']

      if request.POST['campus'] is not None:
        up_obj.current_school_campus = request.POST['campus']

      if request.POST['user_college'] is not None:
        up_obj.current_college = request.POST['user_college']

      if request.POST['user_year'] is not None:
        up_obj.current_school_year = request.POST['user_year']

      if request.POST['living_on_res'] is not None:
        up_obj.living_on_res = request.POST['living_on_res']

      if request.POST['user_job'] is not None:
        up_obj.user_job = request.POST['user_job']

      if request.POST['user_location'] is not None:
        up_obj.user_location = request.POST['user_location']

      if request.POST['current_relationship_status'] is not None:
        up_obj.user_relationship_status = request.POST['current_relationship_status']

      if request.POST['user_description'] is not None:
        up_obj.user_description = request.POST['user_description']
      
      if request.POST['user_interest'] is not None:
        up_obj.user_interests = request.POST['user_interest']     

      # up_obj.user_relationship_status = current_relationship_status
      # up_obj.job_companies = user_job
      # up_obj.user_description = user_description
      # up_obj.user_interests = user_interests
      up_obj.save()

      # else: 
      #   up_obj = UserProfile.objects.create(
      #     user_obj=request.user,
      #     first_name=first_name,
      #     last_name=last_name,
      #     instagram_id=instagram_id, 
      #     snapchat_id=snapchat_id,
      #     spotify_url=spotify_id,
      #     gender=gender, 
      #     current_school_status=current_school_status,
      #     current_school_campus=user_campus,
      #     current_school_year=user_year,
      #     current_college=user_college,
      #     living_on_res=living_on_res,
      #     user_location=user_location,
      #     user_relationship_status=current_relationship_status,
      #     job_companies=user_job,
      #     user_description=user_description,
      #     user_interests=user_interests
      #   )
      #   up_obj.save()


      print('um-list:', user_major_list, len(user_major_list) )
      print('profile-img-list:', user_course_list, profile_images, len(profile_images) )
      if len(user_major_list) > 0:
        um_objects = UserMajors.objects.filter(user_profile_obj = up_obj)
        UserMajors.objects.filter(user_profile_obj = up_obj).delete()  # recreate it

        for user_major in user_major_list:
          um = UserMajors.objects.create(
            user_profile_obj = up_obj,
            major = user_major
          )
          um.save()
      
      if len(user_course_list) > 0:
        uc_objects = UserCourses.objects.filter(user_profile_obj = up_obj)
        UserCourses.objects.filter(user_profile_obj = up_obj).delete() 
        for user_course in user_course_list:
          uc = UserCourses.objects.create(
            user_profile_obj = up_obj,
            course = user_course
          )
          uc.save()

      if len(profile_images) > 0:
        
        UserProfileImage.objects.filter(user_profile_obj = up_obj).delete()
        for fn in profile_images:
          upi = UserProfileImage(
            user_profile_obj = up_obj,
            profile_image=fn
          )
          upi.save()

      return redirect('profile')



    up_obj = UserProfile.objects.get(user_obj=request.user)
    user_first_name = up_obj.first_name
    user_last_name = up_obj.last_name

    user_courses = UserCourses.objects.filter(user_profile_obj=up_obj)
    course_str = ','.join([obj.course for obj in user_courses])
    user_majors = UserMajors.objects.filter(user_profile_obj=up_obj)
    user_major_str = ','.join([obj.major for obj in user_majors])
    user_profile_images = UserProfileImage.objects.filter(user_profile_obj = up_obj).delete()

    user_info = {
      'first_name': user_first_name, 
      'last_name': user_last_name,
      'up_obj': up_obj,
      'user_course_str': course_str,
      'user_major_str': user_major_str
    }
    return render(request, 'edit_profile_two.html', {
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




def logout_view(request):
  logout(request)
  return redirect('landing')




