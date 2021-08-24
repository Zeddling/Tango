import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tango.settings')

import django
django.setup()
from rango.models import Category, Page


def populate():
    #   Steps
    #   1. create lists of dictionaries containing pages we want to add
    #   2.  Create dictionary of dictionaries for categories
    python_pages = [
        {
            "title": "Official Python Tutorials",
            "url": "http://docs.python.org/2/tutorial/",
            "views": 32
        },
        {
            "title":"How to Think like a Computer Scientist",
            "url":"http://www.greenteapress.com/thinkpython/",
            "views": 16
        },
        {
            "title":"Learn Python in 10 Minutes",
            "url":"http://www.korokithakis.net/tutorials/python/",
            "views": 8
        }
    ]


    django_pages = [
        {
            "title":"Official Django Tutorial",
	        "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/", 
            "views": 32
        },
        {
            "title":"Django Rocks",
	        "url":"http://www.djangorocks.com/" , 
            "views": 16
        },
        {
            "title":"How to Tango with Django",
	        "url":"http://www.tangowithdjango.com/", 
            "views": 8
        }
    ]

    rust_pages = [
        {
            "title": "Rust",
            "url": "https://www.rust-lang.org/",
            "views": 40
        }
    ]

    pascal_pages = [
        {
            "title": "Pascal",
            "url": "http://pascal-central.com/ppl/",
            "views": 33
        }
    ]

    php_pages = [
        {
            "title": "PHP",
            "url": "https://www.php.net/",
            "views": 27
        }
    ]

    prolog_pages = [
        {
            "title": "SWI-Prolog",
            "url": "https://www.swi-prolog.org/",
            "views": 10
        },
        {
            "title": "Prolog - Introduction - TutorialsPoint",
            "url": "https://www.tutorialspoint.com/prolog/prolog_introduction.htm",
            "views": 10
        }
    ]

    other_pages = [
        {
            "title":"Bottle", 
            "url":"http://bottlepy.org/docs/dev/", 
            "views": 32
        },
        {
            "title":"Flask", 
            "url":"http://flask.pocoo.org", 
            "views": 16
        }
    ]

    categories ={
        "Python": {
            "pages": python_pages,
            "likes": 64,
            "views": 128
        },
        "Django": {
            "pages": django_pages,
            "likes": 32,
            "views": 64
        },
        "Other Frameworks": {
            "pages": other_pages,
            "likes": 16,
            "views": 48
        },
        "Rust": {
            "pages": rust_pages,
            "likes": 15,
            "views": 40
        },
        "Pascal": {
            "pages": pascal_pages,
            "likes": 13,
            "views": 33
        },
        "Php": {
            "pages": php_pages,
            "likes": 10,
            "views": 27,
        },
        "Prolog": {
            "pages": prolog_pages,
            "likes": 8,
            "views": 20
        }
    }

    for category, category_data in categories.items():
        category = add_category(category, category_data["likes"], category_data["views"])
        for page in category_data["pages"]:
            add_page(category, page["title"], page["url"], page["views"])

    for category in Category.objects.all():
        for page in Page.objects.filter(category=category):
            print("- {0} - {1}".format(str(category), str(page)))

def add_category(name, likes=0, views=0):
    category = Category.objects.get_or_create(name=name)[0]
    category.likes = likes
    category.views = views
    category.save()
    return category

def add_page(category, title, url, views=0):
    page = Page.objects.get_or_create(category=category, title=title)[0]
    page.url = url
    page.views = views
    page.save()
    return page

if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()