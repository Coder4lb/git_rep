from django.shortcuts import render
from .models import Song
# Create your views here.
def index(request):
	posts = Song.objects.all()
	return render( request , 'index.html' , {'post_list' : posts} )