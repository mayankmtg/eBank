from django.db import models


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


class cust_indiv_account(models.Model):
	cust_user_id = models.ForeignKey(user_info, on_delete=models.CASCADE)
	cust_account_type = models.CharField(max_length=250,default="Individual")
	cust_balance = models.FloatField(null=False)


	def __str__(self):
		return self.pk

class merch_org_account(models.Model):
	merch_user_id = models.ForeignKey(user_info, on_delete=models.CASCADE)
	merch_account_type = models.CharField(max_length=250,default="merch/org")
	merch_balance = models.FloatField(null=False)


	def __str__(self):
		return self.pk


class cust_transaction(models.Model):
	transaction_date = models.DateTimeField(null=True)
	from_account_no = models.IntegerField(null=False)
	to_account_no = models.IntegerField(null=False)
	# todo : check on amount
	Amount = models.FloatField(null=False)

	def __str__(self):
		return self.pk
