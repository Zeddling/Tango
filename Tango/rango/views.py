from django.http import request
from django.shortcuts import render
from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page

# Create your views here.
def about(request):
    context_dict = {
        'boldmessage': "About raaaaaaaaa",
        'name': "Victor"
    }

    return render(request, 'rango/about.html', context=context_dict)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm()
        return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=True)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    
    context_dict = {
        'form': form,
        'category': category
    }

    return render(request, 'rango/add_page.html', context_dict)

def index(request):
    categories_by_likes = Category.objects.order_by('-likes')[0:5]
    pages_by_views = Page.objects.order_by('-views')[0:5]

    context_dict = {
        'most_likes': categories_by_likes,
        "most_views": pages_by_views
    }

    return render(request, 'rango/index.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['pages'] = None
    
    return render(request, 'rango/category.html', context_dict)

