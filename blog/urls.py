from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.contrib.auth import views as auth_views
from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required


from blog import views
from blog.models import Post, Comment

urlpatterns = patterns('',
	url(r'^$', views.PostsList.as_view(), name='index'),
	url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
	url(r'^add/$', permission_required('blog:add_post', login_url='/blog/login/') (views.PostCreate.as_view()), name='post_add'),

	url(r'^comment/add/$', views.CommentAdd.as_view(), name='comment_add'),

	url(r'^login/$', views.LoginForm, name='login'),
	url(r'^logout/$', views.Logout, name='logout'),
	url(r'^register/$', views.NewUser, name='register'),	
)