from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse #allows reference to named urls
from .models import User #import the database
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'login/index.html')

def signout_process(request):
    try:
        for key in request.session.keys():
            del request.session[key]
    except:
        pass
    return redirect(reverse('home'))

def signup(request):
    return render(request, 'login/signup.html')

def signin(request):
    return render(request, 'login/signin.html')

def signup_success(request):
    context = {
        'name' : request.session['name']
    }
    return render(request, 'login/signup_success.html', context)

def signup_process(request):
    if request.method == "POST" and request.POST.get('signup'):
        errors = User.objects.register_validator(request.POST)
        if len(errors): #Sign up failed
            # Messages is a one-view temporary holder of information
            for tag, error in errors.iteritems():
                messages.error(request, error)
            return redirect(reverse('signup'))
        else: # Sign up successful
            # Create a new record in the User model database
            User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))

            request.session['name'] = request.POST['first_name']
            return redirect(reverse('signup_success'))

def signin_process(request):
    if request.method == "POST" and request.POST.get('signin'):
        errors = User.objects.login_validator(request.POST)
        if len(errors): # Sign in failed
            for tag, error in errors.iteritems():
                messages.error(request, error)
            return redirect(reverse('signin'))
        else: # Sign in successful
            this_user = User.objects.get(username=request.POST['email'])
            request.session['name'] = this_user.first_name
            request.session['uid'] = this_user.id
            return redirect(reverse('dashboard'))

def dashboard(request):
    # Security measure. Check ID exists in session, otherwise clear session.
    if 'user_id' not in request.session:
        return redirect(reverse('signout_process'))

    context = {
        'name' : request.session['name'],
        'id' : request.session['uid']
    }
    return render(request, 'login/dashboard.html', context)
