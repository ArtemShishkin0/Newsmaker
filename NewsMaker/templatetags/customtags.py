from django import template

register = template.Library()

@register.filter(name='is_moderator')
def is_moderator(user):
    return user.groups.filter(name='Moderators').exists()

