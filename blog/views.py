from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django import forms
from django.forms.util import ErrorList
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group

from blog.models import Post, Comment
from blog.forms import ContactForm

from django.contrib.auth.views import login as login_view, logout

import json


class PostsList(generic.ListView):
	model = Post
	context_object_name = 'latest_posts_list'
	paginate_by = 3

class DetailView(generic.DetailView):
	model = Post
	template_name = 'blog/detail.html'

class PostCreate(generic.edit.CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.pub_date = timezone.now()
		response = super(generic.edit.CreateView, self).form_valid(form)
		return response

class CommentAdd(generic.edit.CreateView):
	model = Comment
	fields = ['content', 'post']

	def form_valid(self, form):
		form.instance.pub_date = timezone.now()
		form.instance.user = self.request.user
		response = super(generic.edit.CreateView, self).form_valid(form)
		return response

def LoginForm(request):
	if not request.user.is_authenticated():
		return login_view(request, template_name='blog/login.html', extra_context = 
				{
					'next': '/blog/'
				}
			)
	else:
		return HttpResponseRedirect( reverse('blog:index') )

def NewUser(request):
	user_creation_form = UserCreationForm(data = request.POST or None)
	if user_creation_form.is_valid():

		new_user = user_creation_form.save()
		commentators = Group.objects.get(name='commentators')
		commentators.user_set.add(new_user)
		
		new_user = authenticate(username=user_creation_form.cleaned_data['username'], 
								password=user_creation_form.cleaned_data['password1'])
		auth_login(request, new_user)

		return HttpResponseRedirect( reverse('blog:index') )
	else:
		return render(request, 'blog/registration.html', {'form': user_creation_form})

def Logout(request):
	return logout(request, next_page=reverse('blog:index'))