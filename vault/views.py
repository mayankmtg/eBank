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
from django.http import Http404
from itertools import chain
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
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
		type_of_req="Register"
		r=registerRequests(user_data=None, first_name=first_name, last_name=last_name, e_mail=e_mail, group=group, type_of_req=type_of_req)
		r.save()
		return HttpResponse("Request Sent")

	return render(request, 'vault/registerRequest.html', context)


@login_required(login_url='/login')
def administrator(request, request_type):
	group=login_success(request)
	if not(request.user.groups.filter(name="Administrator").exists()):
		return group

	valid_types=[
		'Register',
		'Account',
		'Delete',
	]
	if(request_type in valid_types):

		context={
			'request_type': request_type,
			'register_requests':registerRequests.objects.filter(type_of_req=request_type),
		}
		return render(request, 'vault/administrator.html', context)
	else:
		raise Http404("Incorrect Account Type")

@login_required(login_url='/login')
def generateAccountRequest(request):
	group=login_success(request)
	if not (request.user.groups.filter(name="Ind_user").exists() or request.user.groups.filter(name="Organization").exists()):
		# print(request.user.groups.filter(name="Ind_user").exists())
		return group
	type_of_req="Account"
	first_name=request.user.first_name
	last_name=request.user.last_name
	e_mail=request.user.email
	if(request.user.groups.filter(name="Ind_user")):
		group="Ind_user"
	elif(request.user.groups.filter(name="Organization")):
		group="Organization"
	r=registerRequests(user_data=request.user, first_name=first_name, last_name=last_name, e_mail=e_mail, group=group, type_of_req=type_of_req)
	r.save()
	return redirect('vault:vaultExternal')

@login_required(login_url='/login')
def generateDeleteRequest(request):
	group=login_success(request)
	if not (request.user.groups.filter(name="Ind_user").exists() or request.user.groups.filter(name="Organization").exists()):
		# print(request.user.groups.filter(name="Ind_user").exists())
		return group
	type_of_req="Delete"
	first_name=request.user.first_name
	last_name=request.user.last_name
	e_mail=request.user.email
	if(request.user.groups.filter(name="Ind_user")):
		group="Ind_user"
	elif(request.user.groups.filter(name="Organization")):
		group="Organization"
	r=registerRequests(user_data=request.user, first_name=first_name, last_name=last_name, e_mail=e_mail, group=group, type_of_req=type_of_req)
	r.save()
	return redirect('vault:vaultExternal')

@login_required(login_url='/login')
def requestApprove(request, request_type, request_pk):
	group=login_success(request)
	if not(request.user.groups.filter(name="Administrator").exists()):
		return group

	req=get_object_or_404(registerRequests, pk=request_pk)
	if(request_type=="Register"):
		userName=req.first_name[0]+req.last_name[0]+str(req.pk)
		password=get_random_string(length=10)
		new_user=User.objects.create_user(userName,first_name=req.first_name, last_name=req.last_name, password=password, email=req.e_mail)
		group=Group.objects.get(name=req.group)
		group.user_set.add(new_user)
		message="You account has been created\n\n\n User Name:"+userName+"\nPassword:"+password
		subject="Vault Account Successfully Created"
	elif(request_type=="Account"):
		if(req.user_data.groups.filter(name="Ind_user").exists()):
			account_type="Individual"
		elif(req.user_data.groups.filter(name="Organization").exists()):
			account_type="Organization"

		acc=user_account(cust_user_id=req.user_data, cust_account_type=account_type, cust_balance=0)
		acc.save()
		subject="Account Has been Created"
		message="Your Account Has been Created \nAccount Number:" + str(acc)
	elif(request_type=="Delete"):
		subject="Account Deletion"
		user_to_del=req.user_data
		message=""
		try:
			user_to_del.delete()
			message="The user is deleted"
		except User.DoesNotExist:
			message="Error while Processing your delete request"
		except Exception as e: 
			message="Error while Processing your delete request"
		 


	sendEmail(message, req.e_mail, subject)
	req.delete()
	return redirect('vault:administrator', request_type)

@login_required(login_url='/login')
def requestDisapprove(request,request_type, request_pk):
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
		return redirect('vault:administrator', 'Account')



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
	result_trans=cust_transaction.objects.filter(Q(from_account=cust_user) | Q(to_account=cust_user)).filter(pending=False)


	context={
		'account':cust_user,
		'result_trans':result_trans,

	}
	return render(request, 'vault/payments.html', context)

@login_required(login_url='/login')
def support(request, account_no_pk):
	cust_user=user_account.objects.filter(pk=account_no_pk)[0]
	if request.user!=cust_user.cust_user_id:
		return login_success(request)
	if request.method=='POST':
		sendEmail("From: "+str(request.user.email)+"\n"+request.POST['decline_message'],"fcsgrp7@gmail.com", "HELP:"+request.POST['subject'])
		return HttpResponse("Message Sent")
	elif request.method=='GET':
		context={
			'account':cust_user,
		}
		return render(request, 'vault/support.html', context)


@login_required(login_url='/login')
def transferfunds(request, account_no_pk):
	cust_user=user_account.objects.filter(pk=account_no_pk)[0]
	if request.user!=cust_user.cust_user_id:
		return login_success(request)

	context={
		'account':user_account.objects.filter(pk=account_no_pk)[0],
	}
	if request.method=='GET':
		return render(request, 'vault/transfer.html', context)
	if request.method=='POST':
		amount=request.POST['amount']
		account_no=int(request.POST['acno'])
		account_no=account_no-10000000000
		account_from=user_account.objects.filter(pk=account_no_pk)[0]
		if(user_account.objects.filter(pk=int(account_no)).exists()):
			account_to=user_account.objects.filter(pk=account_no)[0]
		else:
			return HttpResponse("Incorrect Account Number")
		otp=int(request.POST['otp'])
		if(amount>0 and OTPVerify(otp)):
			t=cust_transaction(from_account=account_from, to_account=account_to, Amount=int(amount))
			t.save()
			return redirect('vault:accountInfo',account_no_pk)
		else:
			return HttpResponse("Invalid OTP or Amount")
	else:
		HttpResponse("Error")
	
		

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
		otp=int(request.POST['otp'])
		if amount>0 and OTPVerify(otp):
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
	cust_user=user_account.objects.filter(pk=account_no_pk)[0]
	if request.user!=cust_user.cust_user_id:
		return login_success(request)
	totp=OTPSend(cust_user.cust_user_id.email)
	if totp:
		return redirect('vault:vaultDebit', account_no_pk)
	else:
		return HttpResponse("Error")

@login_required(login_url='/login')
def vaultCreditOTP(request, account_no_pk):
	cust_user=user_account.objects.filter(pk=account_no_pk)[0]
	if request.user!=cust_user.cust_user_id:
		return login_success(request)
	totp=OTPSend(cust_user.cust_user_id.email)
	if totp:
		return redirect('vault:vaultCredit', account_no_pk)
	else:
		return HttpResponse("Error")


@login_required(login_url='/login')
def vaultTransferOTP(request, account_no_pk):
	cust_user=user_account.objects.filter(pk=account_no_pk)[0]
	if request.user!=cust_user.cust_user_id:
		return login_success(request)

	totp=OTPSend(cust_user.cust_user_id.email)
	if totp:
		return redirect('vault:transferfunds', account_no_pk)
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
		return redirect('vault:vaultInternal')
	elif request.user.groups.filter(name="Administrator").exists():
		return redirect('vault:administrator', 'Register')
	elif request.user.groups.filter(name="Manager").exists():
		return redirect('vault:vaultManager')
	elif request.user.groups.filter(name="Ind_user").exists():
		return redirect('vault:vaultExternal')
	elif request.user.groups.filter(name="Organization").exists():
		return redirect('vault:vaultExternal')
	else:
		return redirect('/login')