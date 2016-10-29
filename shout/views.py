from django.shortcuts import render
from .forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return home(request)
	else:
		return render(request, "shout/index.html")

def home(request):
	first_name = request.user.first_name;
	return render(request, "shout/home.html",{"first_name":first_name})

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

def user_logout(request):
	logout(request)
	return index(request)