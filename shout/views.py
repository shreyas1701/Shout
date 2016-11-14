from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from .forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile, Shouts, Events
from django.template import RequestContext
from django.utils.timezone import utc
from django.core import serializers
import datetime
import json
from .forms import UserForm, UserProfileForm
from .models import UserProfile, Shouts, Events
from django.views.generic.edit import UpdateView
from django.views import generic
from django.utils.timezone import utc

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return home(request)
    else:
        return render(request, "shout/index.html")

def home(request):
    first_name = request.user.first_name
    shout_list = Shouts.objects.all().order_by('-shout_at')
    event_list = Events.objects.all().order_by('-start_date')
    shouts = change_time(shout_list)
    ctx = {"first_name":first_name, "shout_list":shouts, "event_list":event_list}
    return render(request, "shout/home.html",ctx)

def register(request):
    registered = False
    user_form = UserForm()
    profile_form = UserProfileForm()

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit = False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
        

    context_dict = {'user_form':user_form, 'profile_form':profile_form, 'registered': registered}   
    return render(request, "shout/register.html", context_dict)


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return index(request)
            else:
                return render(request, "shout/login.html", {'message':'Account has been disabled!'})
        else:
            return render(request, "shout/login.html", {'message':'Invalid username or password'})

    else:
        return render(request, "shout/login.html", {})

def shout(request):
    shout_text = request.POST["shout"]
    page = request.POST["pageName"]
    if len (shout_text) > 0 and len(shout_text) <= 160:
        shoutObj = Shouts(shout=shout_text, user=request.user.id, shout_at=datetime.datetime.utcnow().replace(tzinfo=utc))  
        shoutObj.save()
        if page == "profile":
            return profile_view(request)
        else:
            return home(request)

def user_logout(request):
    logout(request)
    return index(request)

def events(request):
    if request.method == "POST":
        event_name = request.POST["eventName"]
        event_descp = request.POST["eventDescription"]
        start_date = request.POST["startDate"]
        end_date = request.POST["endDate"]
        startTime = request.POST["startTime"]
        endTime = request.POST["endTime"]
        location = request.POST["location"]
        invitees = request.POST.getlist('invitees')
        invitees = ','.join(invitees)
        #print(startTime)
        #start = start_date + " " + startTime
        #end = end_date + " " + endTime
        am_pm = startTime[-2:]
        only_time = startTime[:-3]
        start = start_date+"-"+only_time+":"+am_pm
        am_pm_end = endTime[-2:]
        only_time_end = endTime[:-3]
        end = end_date+"-"+only_time_end+":"+am_pm_end
        print(start)
        #print end

        st_date = datetime.datetime.strptime(start, '%m/%d/%Y-%I:%M:%p')
        #dt = datetime.fromtimestamp(mktime(st_date))
        print type(st_date)
        en_date = datetime.datetime.strptime(end, '%m/%d/%Y-%I:%M:%p')
        #print type(en_date)
        eventObj = Events(event_name=event_name, event_descp=event_descp, start_date=st_date, end_date=en_date, username=request.user.first_name, location=location, invitees=invitees)
        eventObj.save()
        print ("i;m saved")
        #except Exception as e:
        #    cont = {"message": ""+str(e)}
        #    return render(request, "shout/events.html", cont)
        return home(request)
    else:
        users = User.objects.all()
        return render(request, "shout/events.html", {'users':users})


class eventsview(generic.ListView):
    template_name = 'shout/myevents.html'
    context_object_name = 'all_events'

    def get_queryset(self):
        return Events.objects.all()


class editEvents(UpdateView):
    model = Events
    fields = ['event_name', 'event_descp', 'start_date', 'end_date', 'username', 'location', 'invitees']


def change_time(shout_list):
    for s in shout_list:
        a = s.shout_at
        b = datetime.datetime.utcnow().replace(tzinfo=utc)
        c = ((b-a).total_seconds())

        if c/86400 < 1:
            if c/3600 < 1:
                if c/60 < 1 and c > 5:
                    s.shout_at = str(int(c))+"s"
                elif int(c) <= 5:
                    s.shout_at = "A few seconds ago!"
                else:
                    s.shout_at = str(int(c/60))+"m"
            else:
                s.shout_at = str(int(c/3600))+"h"
        else:
            s.shout_at = str(int(c/86400))+"d"

        s.user = User.objects.get(id=int(s.user)).first_name

    return shout_list

def profile_view(request):
    loggedUser = request.user
    profile = UserProfile.objects.get(user_id = loggedUser.id)
    shout_list = Shouts.objects.filter(user=loggedUser.id).order_by("-shout_at")
    print shout_list
    shouts = change_time(shout_list)

    context_dict = {'profile':profile,'user':loggedUser, 'shout_list':shouts}
    return render(request, "shout/profile.html", context_dict)

def notify(request):
    context = RequestContext(request)
    loggedUser = request.user
    event_list = Events.objects.all()
    final_list = []
    for e in event_list:
        if str(loggedUser.id) in str(e.invitees):
            final_list.append(e)

    data = serializers.serialize('json', final_list)
    return HttpResponse(data)

def edit_event(request, id):
    if request.method == "POST":
        events(request)
    else:
        context_dict = {}
        event_obj = Events.objects.get(pk=id)
        context_dict = {"current_event":event_obj}
        return render(request,'shout/edit_event.html', context_dict)
