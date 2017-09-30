from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login
from . import views

urlpatterns = [
	# url(r'^login$', views.vaultLogin, name='vaultLogin'),
	url(r'^$', views.vaultHome, name='vaultHome'),
	url(r'login_success/$', views.login_success, name='login_success'),
	url(r'login$', login, {'template_name':'accounts/login.html'}),
	url(r'logout$', auth_views.logout, {'next_page': '/'}, name='logout'),
	url(r'^external/$', views.vaultExternal, name='vaultExternal'),

]
