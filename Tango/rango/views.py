from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render
from django.urls import reverse
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.models import Category, Page

# Create your views here.
def about(request):
    context_dict = {
        'boldmessage': "About raaaaaaaaa",
        'name': "Victor"
    }

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    return render(request, 'rango/about.html', context=context_dict)

@login_required
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

@login_required
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

def get_server_side_cookie(request, cookie, default_val=None):
    value = request.session.get(cookie)
    if not value:
        value = default_val
    return value

def index(request):
    categories_by_likes = Category.objects.order_by('-likes')[0:5]
    pages_by_views = Page.objects.order_by('-views')[0:5]

    context_dict = {
        'most_likes': categories_by_likes,
        "most_views": pages_by_views
    }

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
   
    return render(request, 'rango/index.html', context=context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True
        
        else:
            print(user_form.errors, profile_form.errors)
    
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(
        request,
        'rango/register.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'registered': registered
        }
    )

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text")

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

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return render(request, 'rango/login.html', {'error': 'Incorrect username or password'})
    
    else:
        return render(request, 'rango/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie
        request.session['visits'] = visits