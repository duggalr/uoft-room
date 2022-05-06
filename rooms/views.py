from django.shortcuts import render


def profile(request):
  return render(request, 'profile_new.html')


def main(request):
  return render(request, 'main_new.html')


def browse(request):
  return render(request, 'browse.html')



