from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Trip

# Create your views here.
def index(request):
    return render(request, "beltexam/index.html")

def login(request):
    if request.method == "POST":
        user = User.objects.login(request.POST)
        if not user:
            messages.error(request, "Invalid login credentials!")
        else:
            request.session['logged_user'] = user.id
            # don't need this, unless I'm calling for messages on my "home" page, but I shouldn't because I just have a welcome {{__ }} thang. : messages.success(request, "Welcome {}!".format(user.alias))
            return redirect('/home')
    return redirect('/')


def register(request):
    if request.method == "POST":
        form_errors = User.objects.validate_user_info(request.POST)

    #if there are errors, throw them into flash:
        if len(form_errors) > 0:
            for error in form_errors:
                messages.error(request, error)
        else:
            #register User
            User.objects.register(request.POST)
            messages.success(request, "You have Successfully registered! Please sign-in to continue")

    return redirect('/')


def home(request):
    if "logged_user" not in request.session:
        messages.error(request, "You need to login to see that")
        return redirect('/')
    trips = Trip.objects.all()
    context = {
        'user' : User.objects.get(id=request.session['logged_user']),
        'trips' : trips
    }

    return render(request, 'beltexam/home.html', context)


def add(request):
    if "logged_user" not in request.session:
        messages.error(request, "Gotta login bro")
        return redirect('/')
    trips = Trip.objects.all()
    context = {}
    if trips:
        context = {
            "trips":trips
        }
    return render(request, 'beltexam/add.html', context)

def add_trip(request):
    if "logged_user" not in request.session:
        messages.error(request, "Gotta login bro")
        return redirect('/')
    if request.method == "POST":
        # if request.POST['trip'] != "":
        user = User.objects.get(id=request.session['logged_user'])
        trip = Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], start=request.POST['start'], end=request.POST['end'], user=user)
        return redirect('/home', trip_id=trip.id)

def trips(request, trip_id):
    if "logged_user" not in request.session:
        messages.error(request, "Gotta login bro")
        return redirect('/')

    logged_user = User.objects.get(id=request.session['logged_user'])
    trip = Trip.objects.get(id=trip_id)
    context = {
        "trip" : trip,
        "logged_user" : logged_user
    }
    return render(request, "beltexam/home.html", context)


def logout(request):
    if 'logged_user' in request.session:
        request.session.pop('logged_user')
    return redirect('/')
