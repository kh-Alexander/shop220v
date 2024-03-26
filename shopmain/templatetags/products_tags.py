from django import template
# import shopmain.views as views
# import shopmain.views as views
from shopmain.models import Category

register = template.Library()

@register.inclusion_tag('shopmain/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}
