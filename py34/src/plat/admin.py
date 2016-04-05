from django.contrib import admin
from .models import Song
# Register your models here.

class SongModelAdmin(admin.ModelAdmin):
	list_display = ('title' , 'singer','collection')
	# class Meta:
	# 	model = Song

admin.site.register(Song,SongModelAdmin)