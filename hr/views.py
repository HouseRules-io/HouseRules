from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict

from simple_search import search_filter

from .models import House
from .models import Rulebook
from .models import Rule

from .forms import SignUpForm
from .forms import HouseForm
from .forms import RulebookForm
from .forms import RuleForm


def HelloWorld(request):
    template = loader.get_template('hr/helloworld.html')
    context = {}
    return HttpResponse(template.render(context, request))

def about(request):
	template = loader.get_template('hr/about.html')
	context = {}
	return HttpResponse(template.render(context, request))



# def house(request, House_id):
# 	template = loader.get_template('hr/houseRules.html')
# 	house = get_object_or_404(House, pk=House_id)
# 	rulebook_list = Rulebook.objects.filter(parent_house = House_id)
# 	#rulebook_list = Rulebook.objects.all()
# 	context = {
# 		'House' : house,
# 		'rulebook_list' : rulebook_list
# 	}
# 	return HttpResponse(template.render(context, request)),

def house(request, House_hex):
	house_id = int(House_hex, 16)
	template = loader.get_template('hr/houseRules.html')
	house = get_object_or_404(House, pk=house_id)
	if(request.method == "POST"):
		new_name = request.POST['new_name']
		house.house_name = new_name
		house.save()
	rulebook_list = Rulebook.objects.filter(parent_house = house_id)
	#rulebook_list = Rulebook.objects.all()
	context = {
		'House' : house,
		'rulebook_list' : rulebook_list
	}
	return HttpResponse(template.render(context, request))

def rule(request, Rule_id):
	rule = get_object_or_404(Rule, pk=Rule_id)
	return render(request, 'hr/rule.html', {'Rule': rule})

def rulebook(request, Rulebook_id):
	template = loader.get_template('hr/rulebook.html')
	rulebook = get_object_or_404(Rulebook, pk=Rulebook_id)
	rule_list = Rule.objects.filter(parent_rulebook = Rulebook_id)
	#rule_list = Rule.objects.all()
	context = {
		'Rulebook' : rulebook,
		'rule_list' : rule_list
	}
	return HttpResponse(template.render(context, request))

@login_required
def newHouse(request):
	if request.method == 'POST':
		form = HouseForm(request.POST)
		if form.is_valid():
			new_house = form.save(commit=False)
			new_house.creator = request.user
			new_house.save()
			new_house.init_qr()
			return redirect('/')
	else:
		form = HouseForm()
	return render(request, 'hr/newHouse.html', {'form': form})

@login_required
def newRulebook(request, house_id):
	if request.method == 'POST':
		form = RulebookForm(request.POST)
		if form.is_valid():
			new_rb = form.save(commit=False)
			new_rb.parent_house = House.objects.get(id = house_id)
			if new_rb.parent_house.creator == request.user:
				new_rb.creator = request.user
				new_rb.save()
				return redirect('/house/' + new_rb.parent_house.hex_id + '/')
			else:
				return redirect('/house/' + new_rb.parent_house.hex_id + '/')
	else:
		form = RulebookForm()
	return render(request, 'hr/newRulebook.html', {'form': form})

@login_required
def newRule(request, rb_id):
	if request.method == 'POST':
		form = RuleForm(request.POST)
		if form.is_valid():
			new_r = form.save(commit=False)
			new_r.parent_rulebook = Rulebook.objects.get(id = rb_id)
			if new_r.parent_rulebook.parent_house.creator == request.user:
				new_r.creator = request.user
				new_r.save()
				return redirect('/rulebook/' + rb_id + '/')
			else:
				return redirect('/rulebook/' + rb_id + '/')
	else:
		form = RuleForm()
	return render(request, 'hr/newRule.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'hr/signup.html', {'form': form})

def dev(request):
	template = loader.get_template('hr/dev.html')
	house_list = House.objects.all()
	rulebook_list = Rulebook.objects.all()
	rule_list = Rule.objects.all()

	context = {
		'house_list' : house_list,
		'rulebook_list' : rulebook_list,
		'rule_list' : rule_list
	}
	return HttpResponse(template.render(context, request))


def index(request):
	template = loader.get_template('hr/index.html')
	house_list = House.objects.all()

	context = {
		'house_list' : house_list,
	}

	return HttpResponse(template.render(context, request))

@login_required
def my_houses(request):
	template = loader.get_template('hr/my_houses.html')
	house_list = request.user.profile.my_houses

	context = {
		'house_list' : house_list,
	}

	return HttpResponse(template.render(context, request))

@login_required
def refresh_qr(request):
	for house in House.objects.all():
		house.gen_qr_code()
	return redirect('index')

def add_house(request, house_id):
	house = House.objects.get(id = house_id)
	if request.user.visit_houses.filter(id = house_id).count() > 0:
		request.user.visit_houses.remove(house)
	else:
		request.user.visit_houses.add(house)

	hex_id = hex(house_id)
	return redirect('/house/' + hex_id + "/")

def del_house(request, house_id):
	house = House.objects.get(id = house_id)
	house.delete()
	return redirect('/my_houses/')

def copy_house(request, house_id):
	orig_house = House.objects.get(id = house_id)
	orig_house.copy(request.user)
	
	return redirect('/my_houses/')

def del_rulebook(request, rulebook_id):
	to_del_rb = Rulebook.objects.get(id = rulebook_id)
	to_del_rb.delete()
	return redirect('/my_houses/')

def del_rule(request, rule_id):
	to_del_rule = Rule.objects.get(id = rule_id)
	to_del_rule.delete()
	return redirect('/my_houses/')

def copy_rulebook(request, house_id, rulebook_id):
	house = House.objects.get(id = house_id)
	rb = Rulebook.objects.get(id = rulebook_id)
	rb.copy(house, request.user)
	return redirect('/my_houses/')

def copy_rule(request, rulebook_id):
	return redirect('/my_houses/')

def search(request):
	query = request.GET.get('query', '')
	if(query == ''):
		return redirect('my_houses')

	search_fields = ['house_name']
	houses = House.objects.filter(search_filter(search_fields, query))

	return render(request, 'hr/search_results.html', {"houses":houses, "query":query})