from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from django.db.models.aggregates import Count
from random import randint
import bcrypt

class AlgorithmManager(models.Manager):
    def get_all(self):
        algorithms = Algorithm.objects.all()
        return algorithms

    def show_one(self, request, id):
        this_algorithm = Algorithm.objects.get(id=id)
        return this_algorithm

    def get_random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        random_algo = self.all()[random_index]
        return self.all()[random_index]

    def search(self, request):
        results = Algorithm.objects.get_all()
        if 'search_name' in request.POST:
            results = results.filter(name__icontains=request.POST['search_name'])

        tags = Tag.objects.get_all()
        arr_tags = [];
        for tag in tags:
            if tag.tag in request.POST:
                arr_tags.append(tag.id)
        if len(arr_tags)>0:
            results = results.filter(algorithm_tags__id__in=arr_tags)

        languages = Language.objects.get_all()
        arr_langs = [];
        for language in languages:
            if language.language in request.POST:
                arr_langs.append(language.id)
        if len(arr_langs)>0:
            results = results.filter(algo_solutions__language__id__in=arr_langs)

        return results

class TagManager(models.Manager):
    def get_all(self):
        tags = Tag.objects.all()
        return tags

    def get_one(self, id):
        tag = Tag.objects.get(id=id)
        return tag

    def get_algorithm_tags(self, request, algo_id):
        this_algorithm = Algorithm.objects.get(id=algo_id)
        # algorithm_tags = Tag.objects.filter(tagged_algorithms=this_algorithm)
        algorithm_tags = this_algorithm.algorithm_tags.all()
        return algorithm_tags

class LanguageManager(models.Manager):
    def get_all(self):
        languages = Language.objects.all()
        return languages

    def get_one(self, id):
        language = Language.objects.get(id=id)
        return language

class SolutionManager(models.Manager):
    def validate_solution(self, request):
        validation_messages = []
        if len(request.POST['solution']) < 1:
            validation_messages.append('Solution cannot be empty.')
            return (False, validation_messages)
        else:
            return (True, True)

    def get_solutions(self, request, algo_id):
        this_algorithm=Algorithm.objects.get(id=algo_id)
        solutions = Solution.objects.filter(solution_for=this_algorithm)
        return solutions

class Algorithm(models.Model):
    name = models.CharField(max_length=255)
    statement = models.TextField()
    example = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # algorithm_tags (related name, Tag)
    # algo_solutions (related name, Solution)
    def __str__(self):
        return self.name
    objects = AlgorithmManager()

class Tag(models.Model):
    tag = models.CharField(max_length=255)
    tagged_algorithms = models.ManyToManyField(Algorithm, related_name='algorithm_tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.tag
    objects = TagManager()

class Language(models.Model):
    language = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # language_for (related name, Solution)
    def __str__(self):
        return self.language
    objects = LanguageManager()

class Solution(models.Model):
    solution = models.TextField()
    language = models.ForeignKey(Language, related_name='language_for')  #, null=True
    solution_for = models.ForeignKey(Algorithm, related_name='algo_solutions') # one algo statement can have multiple soluitons, but a solution can only have one algo statement
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.solution
    objects = SolutionManager()
