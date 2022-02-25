from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from articles.models import Article
from users.views import is_moderator


@user_passes_test(is_moderator, redirect_field_name=None)
def article_publish(request):
    if request.method == "GET":
        article = Article.objects.all().filter(active=False).order_by('created')
        context = {"articles": article}
        temlate = loader.get_template('publish_page.html')
        return HttpResponse(temlate.render(context, request))

def article_view_before_publish(request, pk):
    if request.method == "GET":
        choice_list = [val[0] for val in Article.category.field.choices]
        print(choice_list)
        article = Article.objects.get(id=pk)
        context = {'choices': choice_list, 'article': article}
        template = loader.get_template("publish_check.html")
        return HttpResponse(template.render(context, request))