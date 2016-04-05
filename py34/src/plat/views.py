from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Song
# Create your views here.
def index(request):
	posts = Song.objects.all()
	paginator = Paginator(posts, 10) #
	page = request.GET.get('page')
	try :
		post_list = paginator.page(page)
	except PageNotAnInteger :
		post_list = paginator.page(1)
	except EmptyPage :
		post_list = paginator.paginator(paginator.num_pages)
	return render( request , 'index.html' , {'post_list' : post_list} )