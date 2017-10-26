from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login
from . import views

urlpatterns = [
	# url(r'^login$', views.vaultLogin, name='vaultLogin'),
	url(r'^$', views.vaultExternal, name='vaultExternal'),
	url(r'^home/$', views.vaultHome, name='vaultHome'),
	url(r'login/$', login, {'template_name':'accounts/login.html'}),
	url(r'login_success/$', views.login_success, name='login_success'),
	url(r'logout$', auth_views.logout, {'next_page': '/'}, name='logout'),
	url(r'^accounts/(?P<account_no_pk>\d+)/$', views.accountInfo, name='accountInfo'),
	url(r'^accounts/(?P<account_no_pk>\d+)/transferfunds/$', views.transferfunds, name='transferfunds'),
	url(r'^accounts/(?P<account_no_pk>\d+)/debit/$', views.vaultDebit, name='vaultDebit'),
	url(r'^accounts/(?P<account_no_pk>\d+)/credit/$', views.vaultCredit, name='vaultCredit'),
	url(r'^internal/$', views.vaultInternal, name='vaultInternal'),
	url(r'^manager/$', views.vaultManager, name='vaultManager'),
	url(r'^manager/(?P<transaction_pk>\d+)/approve/$', views.vaultTransactionApprove, name='vaultTransactionApproveManager'),
	url(r'^internal/(?P<transaction_pk>\d+)/approve/$', views.vaultTransactionApprove, name='vaultTransactionApprove'),
]	
