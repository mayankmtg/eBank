from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login
from . import views

urlpatterns = [
	# url(r'^login$', views.vaultLogin, name='vaultLogin'),
	url(r'login/$', login, {'template_name':'accounts/login.html'}),
	url(r'register/$', views.vaultRegisterRequest, name='vaultRegisterRequest'),
	url(r'administrator/$', views.administrator, name='administrator'),
	url(r'administrator/requestHandle/(?P<request_pk>\d+)/approve/$', views.requestApprove, name='requestApprove'),
	url(r'administrator/requestHandle/(?P<request_pk>\d+)/disapprove/$', views.requestDisapprove, name='requestDisapprove'),
	url(r'^$', views.vaultExternal, name='vaultExternal'),
	url(r'^home/$', views.vaultHome, name='vaultHome'),
	url(r'login_success/$', views.login_success, name='login_success'),
	url(r'logout$', auth_views.logout, {'next_page': '/'}, name='logout'),
	url(r'^accounts/(?P<account_no_pk>\d+)/$', views.accountInfo, name='accountInfo'),
	url(r'^accounts/(?P<account_no_pk>\d+)/payments/$', views.payments, name='payments'),
	url(r'^accounts/(?P<account_no_pk>\d+)/transferfunds/$', views.transferfunds, name='transferfunds'),
	url(r'^accounts/(?P<account_no_pk>\d+)/debit/$', views.vaultDebit, name='vaultDebit'),
	url(r'^accounts/(?P<account_no_pk>\d+)/debit/otp/$', views.vaultDebitOTP, name='vaultDebitOTP'),
	url(r'^accounts/(?P<account_no_pk>\d+)/credit/$', views.vaultCredit, name='vaultCredit'),
	url(r'^internal/$', views.vaultInternal, name='vaultInternal'),
	url(r'^manager/$', views.vaultManager, name='vaultManager'),
	url(r'^manager/(?P<transaction_pk>\d+)/approve/$', views.vaultTransactionApprove, name='vaultTransactionApproveManager'),
	url(r'^internal/(?P<transaction_pk>\d+)/approve/$', views.vaultTransactionApprove, name='vaultTransactionApprove'),
	url(r'^internal/(?P<transaction_pk>\d+)/disapprove/$', views.vaultTransactionDisapprove, name='vaultTransactionDisapprove'),
]	
