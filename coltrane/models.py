import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
#tagging
from tagging.fields import TagField, Tag
import tagging
#markdown
from markdown import markdown



class Category(models.Model):
	title = models.CharField(max_length=250, help_text ='Make it clever, but keep it under 250 chars.')
	slug = models.SlugField(unique=True, help_text ='Suggested auto-generated from title.  Must be unique.')
	description = models.TextField(help_text = "Put description here. Duh.")

	def live_entry_set(self):
		from coltrane.models import Entry
		return self.entry_set.filter(status = Entry.LIVE_STATUS)

	class Meta:
		ordering = ['title']
		verbose_name_plural = "Categories"



	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return "/categories/%s/" % self.slug

class LiveEntryManager(models.Manager):
	def get_query_set(self):
		return super(LiveEntryManager, self).get_query_set().filter(status = self.model.LIVE_STATUS)

class Entry(models.Model):
	LIVE_STATUS = 1
	DRAFT_STATUS = 2
	HIDDEN_STATUS = 3
	STATUS_CHOICES = (
		(LIVE_STATUS, 'live'),
		(DRAFT_STATUS, 'Draft'),
		(HIDDEN_STATUS, 'Hidden'),
		)
	#managers
	live = LiveEntryManager()
	objects = models.Manager()

	#Core Fields
	title = models.CharField(max_length = 250)
	excerpt = models.TextField(blank=True)
	body = models.TextField()
	pub_date = models.DateTimeField(default = datetime.datetime.now)

	#metadata
	author = models.ForeignKey(User)
	enable_comments = models.BooleanField(default=True)
	featured = models.BooleanField(default=False)
	status = models.IntegerField(choices = STATUS_CHOICES, default = LIVE_STATUS)
	slug = models.SlugField(unique_for_date='pub_date')

	#Categorization
	categories = models.ManyToManyField(Category)
	tags = TagField()

	#fields to store generated HTML
	excerpt_html = models.TextField(editable=False, blank=True)
	body_html = models.TextField(editable=False, blank=True)


	def save(self, force_insert=False, force_update=False):
		self.body_html = markdown(self.body)
		if self.excerpt:
			self.excerpt_html = markdown(self.excerpt)
		super(Entry, self).save(force_insert, force_update)

	class Meta:
		verbose_name_plural = "Entries"
		ordering = ['-pub_date']

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return ('coltrane_entry_detail', (), {'year': self.pub_date.strftime("%Y"),
											   'month': self.pub_date.strftime("%b").lower(),
											   'day': self.pub_date.strftime("%d"),
											   'slug': self.slug })
	get_absolute_url = models.permalink(get_absolute_url)

tagging.register(Entry, tag_descriptor_attr='etags')

class Link(models.Model):
	title = models.CharField(max_length = 250)
	description = models.TextField(blank = True)
	description_html = models.TextField(blank = True)
	url = models.URLField(unique = True)
	posted_by = models.ForeignKey(User)
	pub_date = models.DateTimeField(default = datetime.datetime.now)
	slug = models.SlugField(unique_for_date = 'pub_date')
	tags = TagField()
	enable_comments = models.BooleanField(default = True)
	post_elsewhere = models.BooleanField('Post to Delicious', default = True)
	via_name = models.CharField('Via', max_length = 250, blank = True, help_text = 'The name of the person whose site you spotted the link on.  Optional.')
	via_url = models.URLField('Via URL', blank = True, help_text = 'The URL of the site where you spotted the link')

	class Meta:
		ordering = ['-pub_date']

	def __unicode__(self):
		return self.title

	def save(self):
		if self.description:
			self.description_html = markdown(self.description)
		super(Link, self).save()

	def get_absolute_url(self):
		return('coltrane_entry_detail', (), {'year': self.pub_date.strftime('%Y'),
											 'month': self.pub_date.strftime('%b'),
											 'day': self.pub_date.strftime('%d'),
											 'slug': self.slug })
	get_absolute_url = models.permalink(get_absolute_url)


