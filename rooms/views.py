from django.shortcuts import render




def landing(request):
  return render(request, 'landing.html')


def profile(request):
  return render(request, 'profile_new_one.html')


def main(request):
  return render(request, 'main_new.html')


def browse(request):
  return render(request, 'browse_one.html')


def faq(request):
  return render(request, 'faq.html')



# TODO: 
  # get started with functionality
    # start with login (google + 'inhouse') and then, redirect to profile-edit
      # should have confetti on profile complete 





