from django.core.files.storage import FileSystemStorage
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.decorators import login_required, user_passes_test
from articles.models import Article
from users.views import is_moderator


def article_main(request):
    if request.method == "GET":
        categorySorted = request.session.get('categorysort')
        timeSorted = request.session.get('timesort')

        if not categorySorted and not timeSorted:
            article = Article.objects.all().filter(active=True).order_by('-created')
        elif categorySorted and not timeSorted:
            article = Article.objects.all().filter(category=categorySorted, active=True).order_by('created')
        elif categorySorted and timeSorted:
            if timeSorted == 'Newest':
                article = Article.objects.all().filter(category=categorySorted, active=True).order_by('-created')
            else:
                article = Article.objects.all().filter(category=categorySorted, active=True).order_by('created')
        elif timeSorted:
            if timeSorted == 'Newest':
                article = Article.objects.all().filter(active=True).order_by('-created')
            else:
                article = Article.objects.all().filter(active=True).order_by('created')

        choice_list = [val[0] for val in Article.category.field.choices]
        choice_list = set(choice_list) - {categorySorted}
        context = {"articles": article, "choices": choice_list, "selected": categorySorted, "timesorted": timeSorted}
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
def create(request):
    if request.method == "GET":
        choice_list =  [val[0] for val in Article.category.field.choices]
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
        category = data.get('category')
        article = Article(author=author, title=title, id=id, description=description, content=content, thumbnail=img, category=category, active=False)
        try:
            article.save()
            return redirect('/home')
        except Exception as err:
            print(err)
            return HttpResponse(err)

def article_view(request, pk):
    if Article.objects.get(id=pk, active=True):
        article = Article.objects.get(id=pk)
        context = {'article': article}
        template = loader.get_template('article_view.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse(status=403)


