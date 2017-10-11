from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import user_account



@login_required(login_url='/login')
def vaultHome(request):
	context={
		'accounts':user_account.objects.filter(cust_user_id=request.user),
	}
	return render(request, 'vault/user_home.html', context)


@login_required(login_url='/login')
def vaultExternal(request):
	context={}
	return render(request, 'vault/external.html', context)


@login_required(login_url='/login')
def accountInfo(request, account_no_pk):
	context={
		'account':user_account.objects.filter(pk=account_no_pk)[0],
	}
	return render(request, 'vault/user_account.html', context)

def login_success(request):
	if request.user.groups.filter(name="internal").exists():
		# user is an admin
		return redirect('/')
	else:
		return redirect('/external')