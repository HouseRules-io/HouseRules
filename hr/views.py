from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.

#def helloWorld(request):
#	return HTTPResponse("Hello World!")

def HelloWorld(request):
    template = loader.get_template('hr/helloworld.html')
    context = {}
    return HttpResponse(template.render(context, request))

def houseRules(request, House_id):
	return HttpResponse("You are looking at house %s." % House_id)
