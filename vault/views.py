from django.shortcuts import render
from django.views import generic


def vaultHome(request):
	context={}
	return render(request, 'vault/home.html', context)