from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('categories.html')
def category_list():
    return {'cats': Category.objects.all()}