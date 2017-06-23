import json
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import Algorithm, Tag, Language, Solution #, User
from django.core.urlresolvers import reverse
from django.contrib import messages

def index(request):
    request.session['show_solution'] = False
    tags = Tag.objects.get_all()
    languages = Language.objects.get_all()
    algorithms = Algorithm.objects.get_all()
    context = {
        'tags': tags,
        'languages': languages,
        'algorithms': algorithms,
    }
    return render(request, 'algo_app/index.html', context)

def search(request):
    request.session['show_solution'] = False
    algorithms = Algorithm.objects.search(request)
    context = {
        'algorithms': algorithms,
    }
    return render(request, 'algo_app/results.html', context)

def random(request):
    random_algo = Algorithm.objects.get_random()
    random_id = random_algo.id
    request.session['show_solution'] = False
    return redirect(reverse('algorithm', kwargs={'id': random_id}))

# ALGORITHMS ##################################################################

def show(request, id):
    this_algorithm = Algorithm.objects.show_one(request, id)
    algorithm_tags = Tag.objects.get_algorithm_tags(request, id)
    solutions = Solution.objects.get_solutions(request, id)
    languages = Language.objects.get_all()
    context = {
        'algorithm': this_algorithm,
        'algorithm_tags': algorithm_tags,
        'solutions': solutions,
        'languages': languages,
    }
    return render(request, 'algo_app/algorithm.html', context)

def calculate(request):
    # 1) receive the user's input (stored in request.POST["input"])
    # 2) run a test case through the user's input
    # 3) return the output
    # 4) profit

    # 1)
    print request.POST
    user_input = request.POST["input"]
    print user_input

    # 2) ?

    # 3)
    # return JsonResponse( { "output": ouput } )

    # testing JsonResponse by simply sending the input back and rendering it on the template
    return JsonResponse( {"input":request.POST["input"]} )
