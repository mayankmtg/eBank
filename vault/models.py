from django.db import models
from django.contrib.auth.models import User
import datetime
import redis

lock_table = redis.StrictRedis(host='localhost', port=6379)
class ConcurrentModificationError(ValueError):
    """Base error class for write concurrency errors"""
    pass


class StaleWriteError(ConcurrentModificationError):
    """Tried to write a version of a model that is older than the current version in the database"""
    pass


class AlreadyLockedError(ConcurrentModificationError):
    """Tried to aquire a lock on a row that is already locked"""
    pass


class WriteWithoutLockError(ConcurrentModificationError):
    """Tried to save a lock-required model row without locking it first"""
    pass


class LockedModel:
    """Add row-level locking backed by redis, set lock_required=True to require a lock on .save()"""

    lock_required = False  # whether a lock is required to call .save() on this model

    @property
    def _lock_key(self):
        model_name = self.__class__.__name__
        return '{0}__locked:{1}'.format(model_name, self.id)

    def is_locked(self):
        return lock_table.get(self._lock_key) == b'1'

    def lock(self):
        if self.is_locked():
            raise AlreadyLockedError('Tried to lock an already-locked row.')
        lock_table.set(self._lock_key, b'1')

    def unlock(self):
        lock_table.set(self._lock_key, b'0')

    def save(self, *args, **kwargs):
        if self.lock_required and not self.is_locked():
            raise WriteWithoutLockError('Tried to save a lock-required model row without locking it first')
        super(LockedModel, self).save(*args, **kwargs)


class registerRequests(models.Model):
	user_data = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	first_name = models.CharField(max_length=250, blank=False)
	last_name = models.CharField(max_length=250, blank=False)
	e_mail = models.CharField(max_length=250, blank=False)
	group = models.CharField(max_length=250, blank=False)
	type_of_req=models.CharField(max_length=250, blank=False)

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


class cust_transaction(models.Model, LockedModel):
	lock_required = True
	
	transaction_date = models.DateTimeField(auto_now_add=True, blank=True)
	from_account = models.ForeignKey(user_account, related_name='from_account')
	to_account = models.ForeignKey(user_account, related_name='to_account')
	pending =models.BooleanField(default=True, blank=True)
	# todo : check on amount
	Amount = models.FloatField(null=False)

	def __str__(self):
		return str(self.pk) +", "+ str(self.transaction_date)
