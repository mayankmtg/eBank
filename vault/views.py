from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect




# def vaultHome(request):
# 	context={}
# 	return render(request, 'vault/home.html', context)
# def vaultLogin(request):
# 	context={}
# 	return render(request, 'vault/accounts/login.html', context)

@login_required(login_url='/login')
def vaultHome(request):
	context={}
	return render(request, 'vault/user_home.html', context)

@login_required(login_url='/login')
def vaultExternal(request):
	context={}
	return render(request, 'vault/external.html', context)

def login_success(request):
	if request.user.groups.filter(name="internal").exists():
		# user is an admin
		return redirect('/')
	else:
		return redirect('/external')