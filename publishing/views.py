import os
import re

from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import Group, User

from articles.models import Article, Category
from users.views import is_moderator


@user_passes_test(is_moderator, redirect_field_name=None)
def article_publish(request):
    if request.method == "GET":
        article = Article.objects.all().filter(active=False).order_by('created')
        template = loader.get_template('publish_page.html')
        paginator = Paginator(article, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {"articles": article, "page_obj": page_obj}
        return HttpResponse(template.render(context, request))

def article_view_before_publish(request, pk):
    if request.method == "GET":
        choice_list = Category.objects.all()
        article = Article.objects.get(id=pk)
        selected_choice = article.category.all()
        sel_cat = []
        av_cat = []
        for x in selected_choice:   #костыль
            sel_cat.append(x)
        for z in choice_list:
            av_cat.append(z)
        context = {'choices': set(av_cat)-set(sel_cat), 'article': article, 'selected_choices': sel_cat}
        template = loader.get_template("publish_check.html")
        return HttpResponse(template.render(context, request))


    if request.method == "POST":
        if 'Apply' in request.POST:
            data = request.POST
            article = Article.objects.get(id=pk)
            article.title = data.get('title')
            article.description = data.get('description')
            article.content = data.get('content')
            selected_choice = article.category.all()
            sel_cat = []
            for x in selected_choice:
                sel_cat.append(x)
            article.category.clear()
            for cat in data.getlist('category'):
                if cat not in sel_cat:
                    current_cat = Category.objects.get(name=cat)
                    article.category.add(current_cat)
            article.active = True
            article.save()
            user = User.objects.get(username=article.author)

            html_message = loader.render_to_string(
                'publish_email.html',
                {
                    'article': article,
                }
            )
            send_mail(
                'Your article was published',
                f'Your article "{article.title}" passed moderation and was published. You can find it here: "127.0.0.1:8000/home/article/{article.id}"',
                'theatemsco777@gmail.com',
                [f'{user.email}'],
                html_message=html_message
            )
        elif 'Decline' in request.POST:
            data = request.POST
            article = Article.objects.get(id=pk)
            user = User.objects.get(username=article.author)
            html_message = loader.render_to_string(
                'reject_email.html',
                {
                    'article': article,
                    'reason': data.get("reason")
                }
            )
            send_mail(
                'Your article was rejected',
                f'Your article "{article.title}" was rejected due to the reason: {data.get("reason")}',
                'theatemsco777@gmail.com',
                [f'{user.email}'],
                html_message=html_message
            )
            content_text = re.findall(r'(/uploads/[^"]+)', article.content)
            for photopath in content_text:
                os.remove(f'{os.getcwd()}/media{photopath}')
            article.delete()
        return redirect('/publishing/')
