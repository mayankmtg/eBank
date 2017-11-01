from django.db import models
from django.contrib.auth.models import User
import datetime


class registerRequests(models.Model):
	first_name = models.CharField(max_length=250, blank=False)
	last_name = models.CharField(max_length=250, blank=False)
	e_mail = models.CharField(max_length=250, blank=False)
	group = models.CharField(max_length=250, blank=False)

	def __str__(self):
		return self.first_name + " " + self.last_name

class user_type(models.Model):
	user_super_type = models.CharField(max_length=250, null=False)
	user_type = models.CharField(max_length=250, null=False)

	def __str__(self):
		return self.pk


class user_info(models.Model):
	user_type_id = models.ForeignKey(user_type, on_delete=models.CASCADE)
	user_fname = models.CharField(max_length=250, null=False)
	user_lname =  models.CharField(max_length=250,null=True)
	user_address =  models.CharField(max_length=250, null=False)
	login_id =  models.IntegerField(null=False, unique=True)
	password = models.CharField(max_length=250, null=False)


	def __str__(self):
		return self.pk


class user_account(models.Model):
	cust_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	cust_account_type = models.CharField(max_length=250,default="Individual")
	cust_balance = models.FloatField(null=False)

	# todo : pk not 10 digits
	def __str__(self):
		return str(10000000000+self.pk)


class cust_transaction(models.Model):
	transaction_date = models.DateTimeField(auto_now_add=True, blank=True)
	from_account = models.ForeignKey(user_account, related_name='from_account')
	to_account = models.ForeignKey(user_account, related_name='to_account')
	pending =models.BooleanField(default=True, blank=True)
	# todo : check on amount
	Amount = models.FloatField(null=False)

	def __str__(self):
		return str(self.pk) +", "+ str(self.transaction_date)
