import os
from itertools import chain

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.http.multipartparser import MultiPartParser
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.decorators import login_required, user_passes_test


from NewsMaker.functions import simple_sort, max_limit
from articles.models import *
from users.views import is_moderator
from users.models import Info
from articles.serializers import ArticleSerializer, ArticleCreateSerializer, ArticlePublishSerializer, ProfilesSerializer
from rest_framework import generics, permissions

class profiles_list(generics.ListAPIView):
    serializer_class = ProfilesSerializer

    def get_queryset(self):
        profiles = Info.objects.all()
        return profiles

class profile_detail(generics.RetrieveAPIView):
    serializer_class = ProfilesSerializer

    def get_queryset(self):
        profile = Info.objects.filter(id=self.kwargs["pk"])
        return profile

class article_list(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        articles = Article.objects.filter(active=True)
        return articles


class article_create(generics.CreateAPIView):
    serializer_class = ArticleCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class article_publish_list(generics.ListAPIView):
    serializer_class = ArticlePublishSerializer

    def get_queryset(self):
        articles = Article.objects.filter(active=False)
        return articles

    def check_permissions(self, request):
        if request.user.groups.filter(name='Moderators').exists():
            pass
        else:
            self.permission_denied(request)

class article_publish(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArticlePublishSerializer

    def get_queryset(self):
        article = Article.objects.filter(id=self.kwargs["pk"], active=False)
        return article

    def check_permissions(self, request):
        if request.user.groups.filter(name='Moderators').exists():
            pass
        else:
            self.permission_denied(request)

    # def perform_update(self, serializer):

    # def perform_destroy(self, instance):

class article_detail(generics.RetrieveAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        articles = Article.objects.filter(active=True)
        return articles

def article_main(request):  # view
    if request.method == "GET":

        categorySorted = request.session.get('categorysort')
        timeSorted = request.session.get('timesort')
        article = simple_sort(categorySorted, timeSorted)
        choice_list = Category.objects.all().order_by('name')
        choice_list = [x for x in choice_list if x not in [categorySorted]]
        paginator = Paginator(article, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {"articles": article, "choices": choice_list, "selected": categorySorted, "timesorted": timeSorted,
                   'page_obj': page_obj}
        template = loader.get_template("main.html")
        return HttpResponse(template.render(context, request))
    if request.method == "POST":
        if request.POST['form-id'] == 'Clear':
            if 'categorysort' in request.session:
                del request.session['categorysort']
            if 'timesort' in request.session:
                del request.session['timesort']
        elif request.POST['form-id'] == 'Sort':
            data = request.POST
            categoryChoice = data.get('select-category')
            timeSort = data.get('select-timesort')
            request.session['categorysort'] = categoryChoice
            request.session['timesort'] = timeSort
        return redirect('http://127.0.0.1:8000/home/')


@login_required()
def create(request):  # view
    if request.method == "GET":
        choice_list = Category.objects.all().order_by('name')
        context = {'choices': choice_list, }
        template = loader.get_template("create.html")
        return HttpResponse(template.render(context, request))
    if request.method == "POST":
        img = request.FILES['thumbnail']
        data = request.POST
        author = request.user
        title = data.get('title')
        id = data.get('id')
        description = data.get('description')
        content = data.get('content')
        category = data.getlist('category')
        if max_limit(title, 100) and max_limit(description, 150) and max_limit(content, 30000):
            pass
        else:
            return HttpResponse("Field limit is reached.")
        article = Article(author=author, title=title, id=id, description=description, content=content, thumbnail=img,
                          active=False)
        if is_moderator(author):
            article.active = True
        try:
            article.save()
            article = Article.objects.get(title=title)
            for cat in category:
                current_cat = Category.objects.get(name=cat)
                article.category.add(current_cat)
            return redirect('/home')
        except Exception as err:
            print(err)
            return HttpResponse(err)


def article_view(request, pk):  # view
    if Article.objects.get(id=pk, active=True):
        article = Article.objects.get(id=pk)
        context = {'article': article}
        template = loader.get_template('article_view.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse(status=403)


def search(request):  # view
    if request.method == "GET" and ('?page=' in request.get_full_path()):
        empty = False
        text = request.session.get('text')
        articles = []
        if request.session.get('names') and request.session.get('content'):
            articles.append(Article.objects.filter(title__contains=text))
            articles.append(Article.objects.filter(content__contains=text))
            articles = list(chain(*articles))
            articles.sort(key=lambda x: x.created, reverse=True)
            empty = True
        elif request.session.get('names'):
            articles_o = Article.objects.filter(title__contains=text).order_by('-created')
        elif request.session.get('content'):
            articles_o = Article.objects.filter(content__contains=text).order_by('-created')
        if articles or empty:
            articles_res = articles
        else:
            articles_res = articles_o
        paginator = Paginator(articles_res, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'articles': articles_res, 'page_obj': page_obj}
        template = loader.get_template('main.html')
        return HttpResponse(template.render(context, request))

    elif request.method == "GET":
        context = {}
        template = loader.get_template('search.html')
        return HttpResponse(template.render(context, request))
    if request.method == "POST":
        data = request.POST
        text = data.get('searchtext')
        request.session['text'] = text
        articles = []
        empty = False
        if request.session.get('names'):
            del request.session['names']
        if request.session.get('content'):
            del request.session['content']
        if 'names' in data and 'content' in data:
            articles.append(Article.objects.filter(title__contains=text))
            articles.append(Article.objects.filter(content__contains=text))
            articles = list(chain(*articles))
            articles.sort(key=lambda x: x.created, reverse=True)
            request.session['names'] = True
            request.session['content'] = True
            empty = True
        elif 'names' in data:
            articles_o = Article.objects.filter(title__contains=text).order_by('-created')
            request.session['names'] = True
        elif 'content' in data:
            articles_o = Article.objects.filter(content__contains=text).order_by('-created')
            request.session['content'] = True
        else:
            return HttpResponse("Please select where to search")
        if articles or empty:
            articles_res = articles
        else:
            articles_res = articles_o
        template = loader.get_template('main.html')
        paginator = Paginator(articles_res, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'articles': articles_res, 'page_obj': page_obj, }
        return HttpResponse(template.render(context, request))

