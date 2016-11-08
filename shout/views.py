from django.shortcuts import render
from .forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from .models import Shouts
import datetime
from django.utils.timezone import utc

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return home(request)
	else:
		return render(request, "shout/index.html")

def home(request):
	first_name = request.user.first_name
	shout_list = Shouts.objects.all()

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

	return render(request, "shout/home.html",{"first_name":first_name, "shout_list":shout_list})

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
	if len (shout_text) > 0 and len(shout_text) <= 160:
		shoutObj = Shouts(shout=shout_text, user=request.user.first_name, shout_at=datetime.datetime.utcnow().replace(tzinfo=utc))	
		shoutObj.save()
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
		invitees = request.POST.getlist('invitees')
		for x in invitees:
			print x
		
		try:
			s_month = start_date[0:2]
			s_date = start_date[3:5]
			s_year = start_date[6:] 
			st_date_string = s_year + '-' + s_month + '-' + s_date
			st_date = datetime.strptime(st_date_string, '%Y-%m-%d')
			e_month = end_date[0:2]
			e_date = end_date[3:5]
			e_year = end_date[6:] 
			en_date_string = e_year + '-' + e_month + '-' + e_date
			en_date = datetime.strptime(en_date_string, '%Y-%m-%d')        

		except Exception as e:
			cont = {"message":""+str(e)}

		eventObj = Events(event_name=event_name,event_descp=event_descp,start_date=st_date,end_date=en_date,user=request.user.first_name)
		eventObj.save()
		return home(request)
	else:
		return render(request, "shout/events.html"


def profile_view(request):
	profile = request.user.profile()
	context_dict = {'profile':profile}
	render(request, "shout/profile.html", context_dict)
