from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Song
# Create your views here.
ONE_PAGE_OF_DATA = 10
def index(request):
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
	print(pageType.isdigit() , curPage) 
	posts = Song.objects.all()[startPos:endPos]

	if curPage == 1 and allPage == 1:
		allPostCounts = Song.objects.count()
		allPage = int(allPostCounts / ONE_PAGE_OF_DATA)
		remainPage = allPostCounts % ONE_PAGE_OF_DATA
		if remainPage > 0 :
			allPage += 1

	listnum = range(1,allPage+1)

	return render( request , 'index.html' , {'post_list' : posts , 'listnum':listnum ,'allPage':allPage , 
		'curPage':curPage} )



def loadlyric(request):
	lyric_url = request.GET.get('lyric')
	return HttpResponse(lyric_url, mimetype='application/javascript')
