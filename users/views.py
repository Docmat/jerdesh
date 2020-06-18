from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import UserRegistrationForm


def userAuthorization(request):
	if request.method == 'POST':
		email 		= request.POST.get('email')
		password 	= request.POST.get('password')
		account 	= authenticate(email=email, password=password)
		if account is not None:
			login(request, account)
			return redirect('jerdesh:index_url')
		else:
			message = 'email или пароль введены неверно'
			return render(request, 'users/login.html', {'message': message})
	return render(request, 'users/login.html', {})


def userRegistration(request):
	context = {}
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email 			= form.cleaned_data.get('email')
			raw_password 	= form.cleaned_data.get('password1')
			account 		= authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('jerdesh:index_url')
		else:
			context['registration_form'] = form
	else:
		form = UserRegistrationForm()
		context['registration_form'] = form
	return render(request, 'users/register.html', context)


def userLogout(request):
	logout(request)
	return redirect('jerdesh:index_url')




class UserProfileDetailView(DispatchFuncMixin, DetailView):
    template_name = 'users/user_profile.html'
    model = Profile

    def dispatch(self, request, *args, **kwargs):
        user = 'user'
        return super().dispatch(request, user, *args, **kwargs)