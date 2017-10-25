from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import user_account, cust_transaction



@login_required(login_url='/login')
def vaultHome(request):
	context={
		'accounts':user_account.objects.filter(cust_user_id=request.user),
	}
	return render(request, 'vault/user_home.html', context)


@login_required(login_url='/login')
def vaultInternal(request):
	context={
		'cust_transaction':cust_transaction.objects.filter(Amount__lte=100000, pending=True)
	}
	return render(request, 'vault/internal.html', context)


@login_required(login_url='/login')
def accountInfo(request, account_no_pk):
	context={
		'account':user_account.objects.filter(pk=account_no_pk)[0],
	}
	return render(request, 'vault/user_account.html', context)

@login_required(login_url='/login')
def transferfunds(request, account_no_pk):
	if request.method=='POST':
		amount=request.POST['amount']

		account_no=request.POST['acno']
		account_from=user_account.objects.filter(pk=account_no_pk)[0]
		account_to=user_account.objects.filter(pk=int(account_no))[0]
		print(account_from, account_to)
		t=cust_transaction(from_account=account_from, to_account=account_to, Amount=int(amount))
		t.save()

	context={
		'account':user_account.objects.filter(pk=account_no_pk)[0],
	}
	return render(request, 'vault/user_transfer.html', context)

def login_success(request):
	if request.user.groups.filter(name="Regular").exists():
		# user is an admin
		return redirect('/internal')
	else:
		return redirect('/')