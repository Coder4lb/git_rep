# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Song(models.Model):
	title = models.CharField(max_length = 100) #标题
	singer = models.CharField(max_length = 100) #歌手
	collection = models.CharField(max_length = 100) #专辑
	url = models.FileField(upload_to='songs') #URL
	image = models.ImageField(upload_to='image')
	# lyric = models.FileField

	def __str__(self):
		return self.title
