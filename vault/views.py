from django.http import HttpResponse
from django.contrib.auth.models import Group, User
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from .models import user_account, cust_transaction, registerRequests
from .utils import OTPSend, OTPVerify, sendEmail
from django.utils.crypto import get_random_string

def vaultHome(request):
	context={}
	return render(request, 'vault/home.html', context)

def vaultRegisterRequest(request):
	context={}
	if request.method=='POST':
		first_name=request.POST['first_name']
		last_name=request.POST['last_name']
		e_mail=request.POST['email']
		group=request.POST['group']
		r=registerRequests(first_name=first_name, last_name=last_name, e_mail=e_mail, group=group)
		r.save()
		return HttpResponse("Request Sent")

	return render(request, 'vault/registerRequest.html', context)


@login_required(login_url='/login')
def administrator(request):
	group=login_success(request)
	if not(request.user.groups.filter(name="Administrator").exists()):
		return group
	context={
		'register_requests':registerRequests.objects.all(),
	}
	return render(request, 'vault/administrator.html', context)

@login_required(login_url='/login')
def requestApprove(request, request_pk):
	group=login_success(request)
	if not(request.user.groups.filter(name="Administrator").exists()):
		return group

	req=get_object_or_404(registerRequests, pk=request_pk)
	userName=req.first_name[0]+req.last_name[0]+str(req.pk)
	password=get_random_string(length=10)
	new_user=User.objects.create_user(userName, password=password, email=req.e_mail)
	group=Group.objects.get(name=req.group)
	group.user_set.add(new_user)
	req.delete()
	message="You account has been created\n\n\n User Name:"+userName+"\nPassword:"+password
	sendEmail(message, req.e_mail, "Vault Account Successfully Created")
	return redirect('vault:administrator')

@login_required(login_url='/login')
def requestDisapprove(request, request_pk):
	group=login_success(request)
	if not(request.user.groups.filter(name="Administrator").exists()):
		return group
	
	if (request.method=='GET'):
		context={}
		return render(request, 'vault/requestDisapprove.html', context)

	elif(request.method=='POST'):
		
		req=get_object_or_404(registerRequests, pk=request_pk)
		req.delete()
		sendEmail(request.POST['decline_message'], req.e_mail, request.POST['subject'])
		return redirect('vault:administrator')



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
def payments(request, account_no_pk):
	cust_user=user_account.objects.filter(pk=account_no_pk)[0]
	if request.user!=cust_user.cust_user_id:
		return login_success(request)
	from_trans=cust_transaction.objects.filter(from_account=cust_user).filter(panding=False)
	to_trans=cust_transaction.objects.filter(to_account=cust_user).filter(pending=False)
	context={
		

	}
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
	if request.method=='GET':
		return render(request, 'vault/debit.html', context)

	if request.method=='POST':
		amount=int(request.POST['amount'])
		otp=int(request.POST['otp'])

		if amount>0 and OTPVerify(otp):
			amount=-1*amount
			account_from=user_account.objects.filter(pk=account_no_pk)[0]
			account_to=account_from
			t=cust_transaction(from_account=account_from, to_account=account_to, Amount=int(amount))
			t.save()			
			return redirect('vault:accountInfo', account_no_pk)

		else:
			return HttpResponse("Invalid Amount or OTP")
	else:
		return HttpResponse("Error")


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
def vaultDebitOTP(request, account_no_pk):
	totp=OTPSend()
	if totp:
		return redirect('vault:vaultDebit', account_no_pk)
	else:
		return HttpResponse("Error")

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

@login_required(login_url='/login')
def vaultTransactionDisapprove(request, transaction_pk):
	group=login_success(request)
	if not (request.user.groups.filter(name="Regular").exists() or request.user.groups.filter(name="Manager").exists()):
		# print(request.user.groups.filter(name="Ind_user").exists())
		return group
	transaction=get_object_or_404(cust_transaction, pk=transaction_pk)
	if(request.user.groups.filter(name="Regular").exists() and abs(transaction.Amount)>10000) or (request.user.groups.filter(name="Manager").exists() and abs(transaction.Amount)<=100000):
		return group
	if transaction.pending==True:
		transaction.delete()

	return redirect('vault:vaultInternal')


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