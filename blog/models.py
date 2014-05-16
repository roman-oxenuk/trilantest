from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Post(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()
	pub_date = models.DateTimeField()

	class Meta:
		ordering = ["-pub_date"]

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:index')

class Comment(models.Model):
	post = models.ForeignKey(Post)
	content = models.TextField()
	user = models.ForeignKey(User)
	pub_date = models.DateTimeField(default=timezone.now())

	class Meta:
		ordering = ["pub_date"]

	def get_absolute_url(self):
		return reverse('blog:detail', args=(self.post.pk,))

	def __unicode__(self):
		return self.content