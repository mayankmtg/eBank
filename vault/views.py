from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
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
def vaultTransactionApprove(request, transaction_pk):
	transaction=get_object_or_404(cust_transaction, pk=transaction_pk)
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
		elif to_account==from_account and from_account.cust_balance>=amount:
			from_account.cust_balance=from_account.cust_balance+amount
			from_account.save()
			transaction.pending=False
			transaction.save()
			return redirect('vault:vaultInternal')
		else:
			return HttpResponse("Amount Invalid")
	else:
		return HttpResponse("Transaction Tackled")

def vaultDebit(request):
	
	context={}
	if request.method=='POST':
		amount=int(request.POST['amount'])
		account_no=request.POST['acno']
		if amount>0:
			amount=-1*amount
			account_from=user_account.objects.filter(pk=account_no)
			account_to=account_from
			t=cust_transaction(from_account=account_from, to_account=account_to, Amount=int(amount))
			t.save()			

		else:
			HttpResponse("Invalid Amount")
		# amount=request.POST['amount']
		# account_no=int(request.POST['acno'])
		# amount=abs(int(amount))
		# account=get_object_or_404(user_account, pk=account_no)
		# balance=account.cust_balance
		# if balance >= amount:
		# 	account.cust_balance=balance-amount
		# 	account.save()
		# 	return redirect('vault:vaultDebit')
		# else:
		# 	return HttpResponse("insufficient funds")

	if request.method=='GET':
		return render(request, 'vault/debit.html', context)

def vaultCredit(request):
	context={}
	if request.method=='POST':
		amount=int(request.POST['amount'])
		account_no=request.POST['acno']
		if amount>0:
			account_from=user_account.objects.filter(pk=account_no)[0]
			account_to=account_from
			t=cust_transaction(from_account=account_from, to_account=account_to, Amount=int(amount))
			t.save()			
			return redirect()
		else:
			return HttpResponse("Invalid Amount")
	
	if request.method=='GET':
		return render(request, 'vault/credit.html', context)

def login_success(request):
	if request.user.groups.filter(name="Regular").exists():
		# user is an admin
		return redirect('/internal')
	else:
		return redirect('/')