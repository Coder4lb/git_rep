from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponse , HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Song
from django import forms
from . import recommendations
import json
# Create your views here.


def login_in(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username , password=password)
	if user is not None and user.is_active:
		login( request , user )
	return HttpResponseRedirect( '/index/' )

def logout_out(request):
    logout(request)
    return HttpResponseRedirect("/index/")

ONE_PAGE_OF_DATA = 10
COUNT = 10
def index(request):
	# recommendation for current user
	username = request.user.username
	recom_list = []
	if username == '' or username == None or username == 'admin':
		pass
	else:
		with open("plat/data/rateset.txt" , 'r' ) as data:
			critics = eval(data.read())
		rs = recommendations.getRecommendations(critics , username)[:COUNT]

		with open("plat/data/id_title_set.txt" , 'r' ) as data:
			it = eval(data.read())

		for item in rs:
			id = int(item[1])
			recom_list.append( {'song_id': item[1], 'title' : it[id][0],'singer' : it[id][1],'album' : it[id][2]} )
	
		# page cut and show the songs which the current user had rated
		try:
			curPage = int(request.GET.get('curPage','1'))
			allPage = int(request.GET.get('allPage','1'))
			pageType = str(request.GET.get('pageType',''))
		except ValueError:
			curPage = 1;
			allPage = 1;
			pageType = ''

		if pageType == 'pageDown':
			curPage += 1
		elif pageType == 'pageUp':
			curPage -= 1
		elif pageType.isdigit() :
			curPage = int(pageType)
		
		if curPage <= 0 :
			curPage = 1
		elif curPage > allPage:
			curPage = allPage
			
		startPos = (curPage-1) * ONE_PAGE_OF_DATA
		endPos = startPos + ONE_PAGE_OF_DATA
		postlist = list(critics[username].keys())
		post_list = []
		for id in postlist:
			id = int(id)
			post_list.append( {'song_id': id, 'title' : it[id][0],'singer' : it[id][1],'album' : it[id][2]} )
		posts = post_list[startPos:endPos]

		if curPage == 1 and allPage == 1:
			allPostCounts = len(post_list)
			allPage = int(allPostCounts / ONE_PAGE_OF_DATA)
			remainPage = allPostCounts % ONE_PAGE_OF_DATA
			if remainPage > 0 :
				allPage += 1
		
		listnum = []
		if allPage > 7:
			if 4 < curPage <= allPage-4:
				listnum.append(1)
				listnum.append('...')
				listnum.extend(range(curPage-1,curPage+2))
				listnum.append('...')
				listnum.append(allPage)
			elif curPage <=4 :
				listnum.extend(range(1,6))
				listnum.append('...')
				listnum.append(allPage)
			elif curPage > allPage-4:
				listnum.append(1)
				listnum.append('...')
				listnum.extend(range(allPage-4,allPage+1))
		else:
			listnum = range(1,allPage+1)

	return render( request , 'index.html' , {'post_list' : posts , 'recom_list' : recom_list , 'listnum':listnum ,'allPage':allPage , 
		'curPage':curPage} )
