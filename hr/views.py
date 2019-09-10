from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


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

# def house(request, House_id):
# 	template = loader.get_template('hr/houseRules.html')
# 	house = get_object_or_404(House, pk=House_id)
# 	rulebook_list = Rulebook.objects.filter(parent_house = House_id)
# 	#rulebook_list = Rulebook.objects.all()
# 	context = {
# 		'House' : house,
# 		'rulebook_list' : rulebook_list
# 	}
# 	return HttpResponse(template.render(context, request))

def house(request, House_hex):
	house_id = int(House_hex, 16)
	template = loader.get_template('hr/houseRules.html')
	house = get_object_or_404(House, pk=house_id)
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
def newRulebook(request):
	if request.method == 'POST':
		form = RulebookForm(request.POST)
		if form.is_valid():
			new_rb = form.save(commit=False)
			if new_rb.parent_house.creator == request.user:
				new_rb.creator = request.user
				new_rb.save()
				return redirect('/')
			else:
				return redirect('/')
	else:
		form = RulebookForm()
	return render(request, 'hr/newRulebook.html', {'form': form})

@login_required
def newRule(request):
	if request.method == 'POST':
		form = RuleForm(request.POST)
		if form.is_valid():
			new_r = form.save(commit=False)
			if new_r.parent_rulebook.parent_house.creator == request.user:
				new_r.creator = request.user
				new_r.save()
				return redirect('/')
			else:
				return redirect('/')
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
def refresh_qr(request):
	for house in House.objects.all():
		house.gen_qr_code()
	return redirect('index')
