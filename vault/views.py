from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import user_account, cust_transaction

def vaultHome(request):
	context={}
	return render(request, 'vault/home.html', context)

@login_required(login_url='/login')
def vaultExternal(request):
	group=login_success(request)
	if not (request.user.groups.filter(name="Ind_user").exists() or request.user.groups.filter(name="Organization").exists()):
		# print(request.user.groups.filter(name="Ind_user").exists())
		return group
	context={
		'accounts':user_account.objects.filter(cust_user_id=request.user),
	}
	return render(request, 'vault/external.html', context)


@login_required(login_url='/login')
def vaultInternal(request):
	group=login_success(request)
	if request.user.groups.filter(name="Ind_user").exists() or request.user.groups.filter(name="Organization").exists() or request.user.groups.filter(name="Manager").exists():
		return group

	context={
		'cust_transaction':cust_transaction.objects.filter(Amount__lte=100000, pending=True) & cust_transaction.objects.filter(Amount__gte=-100000, pending=True),
	}
	return render(request, 'vault/internal.html', context)


@login_required(login_url='/login')
def vaultManager(request):
	group=login_success(request)
	if request.user.groups.filter(name="Ind_user").exists() or request.user.groups.filter(name="Organization").exists() or request.user.groups.filter(name="Regular").exists():
		return group

	context={
		'cust_transaction':cust_transaction.objects.filter(Amount__gt=100000, pending=True) | cust_transaction.objects.filter(Amount__lt=-100000, pending=True),
	}
	return render(request, 'vault/internal.html', context)


@login_required(login_url='/login')
def accountInfo(request, account_no_pk):
	cust_user=user_account.objects.filter(pk=account_no_pk)[0]
	if request.user!=cust_user.cust_user_id:
		return login_success(request)
	context={
		'account':cust_user,
	}
	return render(request, 'vault/accountInfo.html', context)

@login_required(login_url='/login')
def transferfunds(request, account_no_pk):
	cust_user=user_account.objects.filter(pk=account_no_pk)[0]
	if request.user!=cust_user.cust_user_id:
		return login_success(request)
	if request.method=='POST':
		amount=request.POST['amount']

		account_no=request.POST['acno']
		account_from=user_account.objects.filter(pk=account_no_pk)[0]
		account_to=user_account.objects.filter(pk=int(account_no))[0]
		print(account_from, account_to)
		t=cust_transaction(from_account=account_from, to_account=account_to, Amount=int(amount))
		t.save()
		return redirect('vault:accountInfo',account_no_pk)
	context={
		'account':user_account.objects.filter(pk=account_no_pk)[0],
	}
	return render(request, 'vault/transfer.html', context)

@login_required(login_url='/login')
def vaultDebit(request, account_no_pk):
	cust_user=user_account.objects.filter(pk=account_no_pk)[0]
	if request.user!=cust_user.cust_user_id:
		return login_success(request)
	context={
		'account':cust_user,
	}
	if request.method=='POST':
		amount=int(request.POST['amount'])
		if amount>0:
			amount=-1*amount
			account_from=user_account.objects.filter(pk=account_no_pk)[0]
			account_to=account_from
			t=cust_transaction(from_account=account_from, to_account=account_to, Amount=int(amount))
			t.save()			
			return redirect('vault:accountInfo',account_no_pk)

		else:
			HttpResponse("Invalid Amount")

	if request.method=='GET':
		return render(request, 'vault/debit.html', context)

@login_required(login_url='/login')
def vaultCredit(request, account_no_pk):
	cust_user=user_account.objects.filter(pk=account_no_pk)[0]
	if request.user!=cust_user.cust_user_id:
		return login_success(request)
	context={
		'account':cust_user,
	}
	if request.method=='POST':
		amount=int(request.POST['amount'])
		if amount>0:
			account_from=user_account.objects.filter(pk=account_no_pk)[0]
			account_to=account_from
			t=cust_transaction(from_account=account_from, to_account=account_to, Amount=int(amount))
			t.save()			
			return redirect('vault:accountInfo',account_no_pk)
		else:
			return HttpResponse("Invalid Amount")
	
	if request.method=='GET':
		return render(request, 'vault/credit.html', context)

@login_required(login_url='/login')
def vaultTransactionApprove(request, transaction_pk):
	group=login_success(request)
	if not (request.user.groups.filter(name="Regular").exists() or request.user.groups.filter(name="Manager").exists()):
		# print(request.user.groups.filter(name="Ind_user").exists())
		return group

	transaction=get_object_or_404(cust_transaction, pk=transaction_pk)
	if(request.user.groups.filter(name="Regular").exists() and abs(transaction.Amount)>10000) or (request.user.groups.filter(name="Manager").exists() and abs(transaction.Amount)<=100000):
		return group
	if(transaction.pending==True):
		from_account=transaction.from_account
		to_account=transaction.to_account
		amount=transaction.Amount
		date=transaction.transaction_date
		if amount>0 and to_account!=from_account and from_account.cust_balance>=amount:
			to_account.cust_balance=to_account.cust_balance+amount
			from_account.cust_balance=from_account.cust_balance-amount
			to_account.save()
			from_account.save()
			transaction.pending=False
			transaction.save()
			return redirect('vault:vaultInternal')
		elif to_account==from_account and from_account.cust_balance+amount>=0:
			from_account.cust_balance=from_account.cust_balance+amount
			from_account.save()
			transaction.pending=False
			transaction.save()
			return redirect('vault:vaultInternal')
		else:
			return HttpResponse("Amount Invalid")
	else:
		return HttpResponse("Transaction Tackled")



def login_success(request):
	if request.user.groups.filter(name="Regular").exists():	
		return redirect('/internal')
	elif request.user.groups.filter(name="Administrator").exists():
		return redirect('/administrator')
	elif request.user.groups.filter(name="Manager").exists():
		return redirect('/manager')
	elif request.user.groups.filter(name="Ind_user").exists():
		return redirect('/')
	elif request.user.groups.filter(name="Organization").exists():
		return redirect('/')
	else:
		return redirect('/login')