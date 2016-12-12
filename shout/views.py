from django.shortcuts import render,render_to_response, get_object_or_404
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
from .models import *
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
    loggedUser = request.user
    
    event_list = Events.objects.all().order_by('-start_date')
    #shouts = change_time(shout_list)
    shouts_num = len(Shouts.objects.filter(user=request.user.id))
    follower = len(FollowMap.objects.filter(following=loggedUser.id))
    following = len(FollowMap.objects.filter(follower=loggedUser.id))
    flwList = get_follow_list(loggedUser.id)
    ctx = {"event_list":event_list, "shouts_num":shouts_num, "follower":follower, "following":following, "flwList":flwList}
    return render(request, "shout/home.html",ctx)

def get_follow_list(id):
    follow_list = []
    for x in User.objects.all():
        if x.id != id and x.first_name != "":
            try:
                flwMp = FollowMap.objects.get(follower=id, following=x.id)
            except FollowMap.DoesNotExist:
                follow_list.append(x)

    return follow_list
        


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
            return profile_view(request, request.user.id)
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
        invis = request.POST["invis"]
        invitees = []
        if int(str(invis[0])) == 0:
            for x in User.objects.all():
                invitees.append(str(x.id))
        else:
            invitees = request.POST.getlist("invitees")

        invitees = ','.join(invitees)

        am_pm = startTime[-2:]
        only_time = startTime[:-3]
        start = start_date+"-"+only_time+":"+am_pm
        am_pm_end = endTime[-2:]
        only_time_end = endTime[:-3]
        end = end_date+"-"+only_time_end+":"+am_pm_end
        st_date = datetime.datetime.strptime(start, '%m/%d/%Y-%I:%M:%p')        
        en_date = datetime.datetime.strptime(end, '%m/%d/%Y-%I:%M:%p')
        
        eventObj = Events(event_name=event_name, event_descp=event_descp, start_date=st_date, end_date=en_date, username=request.user.first_name, location=location, invitees=invitees)
        eventObj.save()
        create_notif(invitees.split(","), "events", eventObj)
        return home(request)
    else:
        users = User.objects.all()
        return render(request, "shout/events.html", {'users':users})


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

        s.username = User.objects.get(id=int(s.user)).first_name

    return shout_list

def create_notif(ppl_list, type, obj):
    when = datetime.datetime.now()
    notif_text = ""
    if type == "events":
        notif_text = ""+str(obj.username)+" has invited you to: "+str(obj.event_name)

    elif type == "likes":
        notif_text = ""+str(User.objects.get(id=obj.liker).first_name)+" has liked your shout"

    notif_obj = Notification(notif_text = notif_text, when=when)
    notif_obj.save()

    for x in ppl_list:
        user = x
        nm_obj = NotifMap(user = user, notif = notif_obj, seen=False)
        nm_obj.save()

def profile_view(request, id):
    loggedUser = request.user
    profile = UserProfile.objects.get(user_id = id)
    shout_list = Shouts.objects.filter(user=id).order_by("-shout_at")
    user_prof = User.objects.get(id=id)
    shouts = change_time(shout_list)
    following = False
    try:
        flwMp = FollowMap.objects.filter(follower=loggedUser.id)
    except FollowMap.DoesNotExist:
        flwMp = None

    if flwMp:
        following = True

    context_dict = {'profile':profile,'loggedUser':loggedUser, "user_prof":user_prof, 'shout_list':shouts, "following":following}
    return render(request, "shout/profile.html", context_dict)

def notify(request):
    notMapObj = NotifMap.objects.filter(user=request.user.id)
    final_list = []
    for x in notMapObj:
        
        notif_text = Notification.objects.get(id=x.notif.id).notif_text
        seen = x.seen

        final_list.append({"notif_text":str(notif_text), "seen":""+str(seen)})

    
    return HttpResponse(str(final_list))

def edit_event(request, id):
        context_dict = {}
        event_obj = Events.objects.get(pk=id)       
        st_date = event_obj.start_date.date()
        st_date = st_date.strftime('%m/%d/%Y')
        en_date = event_obj.end_date.date()
        en_date = en_date.strftime('%m/%d/%Y')
        st_time = event_obj.start_date.time()
        en_time = event_obj.end_date.time()
        users = User.objects.all()
        context_dict = {"current_event": event_obj, "users": users, "st_date":st_date, "en_date" :en_date,"st_time":st_time, "en_time" :en_time}
        return render(request, 'shout/edit_event.html', context_dict)


def updateevent(request):
    if request.method == "POST":
        id = request.POST["eventID"]
        eventobj = Events.objects.get(id=id)
        eventobj.event_name = request.POST["eventName"]
        eventobj.event_descp = request.POST["eventDescription"]
        start_date = request.POST["startDate"]
        end_date = request.POST["endDate"]
        startTime = request.POST["startTime"]
        endTime = request.POST["endTime"]
        eventobj.location = request.POST["location"]
        invitees = request.POST.getlist('invitees')
        eventobj.invitees = ','.join(invitees)
        am_pm = startTime[-2:]
        only_time = startTime[:-3]
        start = start_date+"-"+only_time+":"+am_pm
        am_pm_end = endTime[-2:]
        only_time_end = endTime[:-3]
        end = end_date+"-"+only_time_end+":"+am_pm_end
        st_date = datetime.datetime.strptime(start, '%m/%d/%Y-%I:%M:%p')
        en_date = datetime.datetime.strptime(end, '%m/%d/%Y-%I:%M:%p')
        eventobj.start_date = st_date
        eventobj.end_date = en_date

        eventobj.save()
        #create_notif(invitees.split(","), "events", eventobj)
        return home(request)

def updateSeen(request):
    notMapObj = NotifMap.objects.filter(user=request.user.id)
    
    for x in notMapObj:
        if not x.seen:
            x.seen = True
            x.save()

    return HttpResponse("success")

def hashResults(request, text):

    loggedUser= request.user

    shouts_num = len(Shouts.objects.filter(user=loggedUser.id))
    follower = len(FollowMap.objects.filter(following=loggedUser.id))
    following = len(FollowMap.objects.filter(follower=loggedUser.id))

    cont = {"shouts_num":shouts_num,"follower":follower, "following":following, "hashText":text}

    return render(request, "shout/hashResults.html",cont)

def followUser(request, id):
    
    loggedUser = request.user.id
    flwngUser = User.objects.get(id=id)
    try:
        flwMp = FollowMap.objects.get(follower=loggedUser, following=id)
    except FollowMap.DoesNotExist:
        flwMp = None

    if flwMp:
        flwMp.delete();    
    else:
        if flwngUser:
            follow = FollowMap(follower=loggedUser, following=id)
            follow.save()

    return profile_view(request, id)

def like(request):
    loggedUser = request.user.id
    id = request.POST["id"]
    shout = Shouts.objects.get(id=id)
    likes = Likers(liker = loggedUser, shout_id=id )
    likes.save()
    shout.likes += 1
    shout.save()
    create_notif(shout.user, "likes", likes)
    return HttpResponse("Success")

def unlike(request):
    loggedUser = request.user.id
    id = request.POST["id"]
    shout = Shouts.objects.get(id=id)
    likes = Likers.objects.get(liker = loggedUser, shout_id=id )
    likes.delete()
    shout.likes -= 1
    shout.save()
    return HttpResponse("Success")

def getShouts(request):
    loggedUser = request.user
    location = request.POST["location"]
    shout_list = []

    if location == "home":
        flw_list = FollowMap.objects.filter(follower=loggedUser.id)
        for i in Shouts.objects.filter(user=loggedUser.id).order_by('-shout_at'):
            shout_list.append(i)

        for x in flw_list:
            shous = Shouts.objects.filter(user=x.following).order_by('-shout_at')
            for y in shous:
                shout_list.append(y)


    elif location == "profile":
        userId = request.POST["userId"]
        for i in Shouts.objects.filter(user=userId).order_by('-shout_at'):
            shout_list.append(i)

    elif location == "hashtag":
        hashText = request.POST["hashText"]
        for i in Shouts.objects.filter(shout__contains = hashText).order_by("-shout_at"):
            shout_list.append(i)

    shouts = change_time(shout_list)
    shoutList = []
    for x in shouts:
        liked = False
        if Likers.objects.filter(liker=loggedUser.id, shout_id=x.id):
            liked = True

        shoutList.append(objToDict(x, liked))

    return HttpResponse(str(shoutList))

def objToDict(obj, liked):

    objDict = {}
    shout_text = str(obj.shout).replace("'", "%")
    objDict["id"] = int(obj.id)
    objDict["shout"] = shout_text
    objDict["user"] = str(obj.user)
    objDict["shout_at"] = obj.shout_at
    objDict["likes"] = int(obj.likes)
    objDict["username"] = str(obj.username)
    objDict["liked"] = str(liked)

    return objDict

def event_info(request, id):

    event_obj = Events.objects.get(pk=id)
    context_dict = {"event": event_obj}
    return render(request, 'shout/event_info.html', context_dict)

def myevents(request):

    myevent = Events.objects.filter(username=request.user.first_name)
    context = {"event_list": myevent}

    return render(request, "shout/myevents.html", context)

def getEvents(request):

    event_list = []
    hashText = request.POST["hashText"]
    for i in Events.objects.filter(event_name__contains=hashText):
        event_list.append(objToDicttwo(i))
    return HttpResponse(str(event_list))

def objToDicttwo(obj):

   objdict = {}
   objdict["id"] = int(obj.id)
   objdict["event_name"] = str(obj.event_name)
   objdict["description"] = str(obj.event_descp)

   return objdict
