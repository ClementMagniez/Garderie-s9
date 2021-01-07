from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render, get_object_or_404
from ..models import Child, Parent, HourlyRate, Schedule, ReliablePerson
from django.urls import reverse
from django.views.generic import RedirectView
from django.utils import timezone
from django.views.generic.detail import SingleObjectMixin
from ..forms import *

# Contient les views redirigeant l'utilisateur'


# Redirection accueil -> login
class HomeRedirectView(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		return reverse('login')



# Appelle ChildManager#generate_monthly_bills et renvoie sur admin_index
# TODO : remplacer par une requête AJAX ?
class NewMonthlyBillsView(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		Child.objects.generate_monthly_bills()		
		return reverse('admin_index')

# Redirection après le login selon le type d'utilisateur
class IndexRedirectView(RedirectView):	
	def get_redirect_url(self, *args, **kwargs):
		user=self.request.user
		if user.is_superuser:
			return reverse('admin_index')
		elif user.is_staff:
			return reverse('educ_index')
		else:
			return reverse('parent_index')

# Redirection après le login selon le type d'utilisateur
class IndexRedirectView(RedirectView):	
	def get_redirect_url(self, *args, **kwargs):
		user=self.request.user
		if user.is_superuser:
			return reverse('admin_index')
		elif user.is_staff:
			return reverse('educ_index')
		else:
			return reverse('parent_index')

# TODO Voir s'il ne serait pas tout aussi simple de 
# se débarrasser de EducRedirect et ParentRedirect

# Redirection d'une éducatrice
class EducRedirectView(RedirectView):
	
	def get_redirect_url(self, *args, **kwargs):
		return reverse('children_list')

# Redirection d'un parent
class ParentRedirectView(RedirectView):
	
	def get_redirect_url(self, *args, **kwargs):
		user=self.request.user
		return reverse('parent_profile', args=[user.id])		


