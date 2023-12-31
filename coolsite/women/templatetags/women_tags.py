from django import template
from women.models import *
from django.db.models import Count

register = template.Library()


@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
    else:
        cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0).order_by(sort)

    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('women/list_tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}
