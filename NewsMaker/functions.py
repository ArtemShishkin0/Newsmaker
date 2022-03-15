import os
import regex as re

from articles.models import Article

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def simple_sort(categorySorted, timeSorted, Article=Article):
    if not categorySorted and not timeSorted:
        article = Article.objects.all().filter(active=True).order_by('-created')
    elif categorySorted and not timeSorted:
        article = Article.objects.all().filter(category__name=categorySorted, active=True).order_by('created')
    elif categorySorted and timeSorted:
        if timeSorted == 'Newest':
            article = Article.objects.all().filter(category__name=categorySorted, active=True).order_by('-created')
        else:
            article = Article.objects.all().filter(category__name=categorySorted, active=True).order_by('created')
    elif timeSorted:
        if timeSorted == 'Newest':
            article = Article.objects.all().filter(active=True).order_by('-created')
        else:
            article = Article.objects.all().filter(active=True).order_by('created')
    return article


def is_moderator(user):
    return user.groups.filter(name='Moderators').exists()

def remove_photo(photo):
    try:
        os.remove(photo.path)
    except Exception as err:
        print(err)
    pass

def max_limit(content, limit):
    return len(content) <= limit

def match_regex(content, pattern):
    return re.match(rf'{pattern}', content)