from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse


from .models import House
from .models import Rulebook
from .models import Rule

# Create your views here.

#def helloWorld(request):
#	return HTTPResponse("Hello World!")

def HelloWorld(request):
    template = loader.get_template('hr/helloworld.html')
    context = {}
    return HttpResponse(template.render(context, request))

def houseRules(request, House_id):
	house = get_object_or_404(House, pk=House_id)
	rulebooks = Rulebook.objects.filter(parent_house = House_id)
	return render(request, 'hr/houseRules.html', {'House':house}, {'Rulesbooks':rulebooks})

def rule(request, Rule_id):
	rule = get_object_or_404(Rule, pk=Rule_id)
	return render(request, 'hr/rule.html', {'Rule': rule})

def rulebook(request, Rulebook_id):
	rulebook = get_object_or_404(Rulebook, pk=Rulebook_id)
	rules = Rule.objects.filter(parent_rulebook = Rulebook_id)
	return render(request, 'hr/rulebook.html', {'Rulebook': rulebook}, {'Rules' : rules})







def home(request):
	template = loader.get_template('hr/index.html')
	house_list = House.objects.all()
	rulebook_list = Rulebook.objects.all()
	rule_list = Rule.objects.all()

	context = {
		'house_list' : house_list,
		'rulebook_list' : rulebook_list,
		'rule_list' : rule_list
	}
	return HttpResponse(template.render(context, request))
