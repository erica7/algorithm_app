from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from django.db.models.aggregates import Count
from random import randint
import bcrypt


# to do: capitalize algorithm name and tag when creating entries


class AlgorithmManager(models.Manager):
    def get_all(self):
        algorithms = Algorithm.objects.all()
        return algorithms

    def validate_algorithm(self, request):
        validation_messages = []
        if len(request.POST['name']) < 1:
            validation_messages.append('Name cannot be empty.')
            return (False, validation_messages)
        elif len(request.POST['statement']) < 1:
            validation_messages.append('Statement cannot be empty.')
            return (False, validation_messages)
        elif len(request.POST['example']) < 1:
            validation_messages.append('Example cannot be empty.')
            return (False, validation_messages)
        elif len(request.POST['solution']) < 1:
            validation_messages.append('Solution cannot be empty.')
            return (False, validation_messages)
        else:
            try:
                Algorithm.objects.get(name__iexact=request.POST['name'])
                validation_messages.append("Algorithm already exists.")
                return (False, validation_messages)
            except MultipleObjectsReturned:
                validation_messages.append("Algorithm already exists. (multiple instances)")
                return (False, validation_messages)
            except ObjectDoesNotExist:
                return (True, True)

    def create_algorithm(self, request):
        this_algorithm = Algorithm.objects.create(name=request.POST['name'], statement=request.POST['statement'], example=request.POST['example'])
        tags = Tag.objects.get_all()
        for tag in tags:
            if tag.tag in request.POST:
                this_tag = Tag.objects.get(tag=tag.tag)
                this_algorithm.algorithm_tags.add(this_tag)
        return (True, this_algorithm.id) ###

    def show_one(self, request, id):
        this_algorithm = Algorithm.objects.get(id=id)
        return this_algorithm

    def get_random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        random_algo = self.all()[random_index]
        return self.all()[random_index]

    def update(self, request):
        pass

    def destroy(self, request, id):
        # delete all associated solutions
        Solution.objects.destroy_all_solutions(request,id)
        Algorithm.objects.get(id=id).delete()
        return (True, True)

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

    def create_tag(self, request):
        validation_messages = []
        if len(request.POST['tag']) < 1:
            validation_messages.append('Tag cannot be empty.')
            return (False, validation_messages)
        else:
            try:
                Tag.objects.get(tag__iexact=request.POST['tag'])
                validation_messages.append("Tag already exists.")
                return (False, validation_messages)
            except MultipleObjectsReturned:
                validation_messages.append("Tag already exists. (multiple instances)")
                return (False, validation_messages)
            except ObjectDoesNotExist:
                Tag.objects.create(tag=request.POST['tag'])
                return (True, True)

    def update_tag(self, request, id):
        this_tag = Tag.objects.get(id=id)
        this_tag.tag = request.POST['new_value']
        this_tag.save()
        return (True, True)

    def destroy_tag(self, request):
        Tag.objects.get(id=id).delete()
        return (True, True)

class LanguageManager(models.Manager):
    def get_all(self):
        languages = Language.objects.all()
        return languages

    def get_one(self, id):
        language = Language.objects.get(id=id)
        return language

    def create_language(self, request):
        validation_messages = []
        if len(request.POST['language']) < 1:
            validation_messages.append('Language cannot be empty.')
            return (False, validation_messages)
        else:
            try:
                Language.objects.get(language__iexact=request.POST['language'])
                validation_messages.append("Language already exists.")
                return (False, validation_messages)
            except MultipleObjectsReturned:
                validation_messages.append("Language already exists. (multiple instances)")
                return (False, validation_messages)
            except ObjectDoesNotExist:
                Language.objects.create(language=request.POST['language'])
                return (True, True)

    def update_language(self, request, id):
        this_language = Language.objects.get(id=id)
        this_language.language = request.POST['new_value']
        this_language.save()
        return (True, True)

    def destroy_language(self, request, id):
        Language.objects.get(id=id).delete()
        return (True, True)

class SolutionManager(models.Manager):
    def validate_solution(self, request):
        validation_messages = []
        if len(request.POST['solution']) < 1:
            validation_messages.append('Solution cannot be empty.')
            return (False, validation_messages)
        else:
            return (True, True)

    def create_solution(self, request, algo_id):
        this_algorithm = Algorithm.objects.get(id=algo_id)
        this_language = Language.objects.get(language=request.POST['language'])
        this_solution = Solution.objects.create(solution=request.POST['solution'], language=this_language, solution_for=this_algorithm)
        return (True, True)

    def get_solutions(self, request, algo_id):
        this_algorithm=Algorithm.objects.get(id=algo_id)
        solutions = Solution.objects.filter(solution_for=this_algorithm)
        return solutions

    def destroy_all_solutions(self, request, algo_id):
        # all_solutions = Solution.objects.get_solutions(request, algo_id)
        # print 'all solutions for the algorithm are ', all_solutions
        Solution.objects.get_solutions(request, algo_id).delete()
        return (True, True)

    def destroy_one_solution(self, request, solution_id):
        Solution.objects.get(id=solution_id).delete()
        return (True, True)

class UserManager(models.Manager):
    def create_admin(self):
        try:
            User.objects.get(username='admin')
            return
        except MultipleObjectsReturned:
            return
        except ObjectDoesNotExist:
            hashed = bcrypt.hashpw('passwordforalgorithms'.encode(), bcrypt.gensalt())
            admin = User.objects.create(username='admin', password=hashed)
            return

    def login(self,request):
        user = User.objects.get(username='admin')
        if user.password == bcrypt.hashpw(request.POST['admin_password'].encode(), user.password.encode()):
            return True
        return False

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

class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.username
    objects = UserManager()
