from django.contrib.auth.models import User
from rango.bing_search import get_results
from datetime import datetime
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import redirect, render
from django.urls import reverse
from rango.forms import CategoryForm, PageForm, UserProfileForm
from rango.models import Category, Page, UserProfile
from registration.backends.simple.views import RegistrationView


#   Handle on register redirection
class ModifiedRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('register_profile')


# Create your views here.
def about(request):
    context_dict = {
        'boldmessage': "About rango",
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

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')
    
    profile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({
        'website': profile.website,
        'picture': profile.picture
    })

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)
    
    return render(request, 'rango/profile.html', {
        'profile': profile,
        'selectedUser': user,
        'form': form
    })

@login_required
def search(request, category_name_slug):
    results = []

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            results = get_results(query)
    
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['pages'] = None
    
    context_dict['results'] = results
    
    return render(request, 'rango/category.html', context_dict)

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

def track_url(request):
    page_id = None

    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']

    if page_id:
        try:
            page = Page.objects.get(id=page_id)
            page.views = page.views + 1
            page.save()
            return redirect(page.url)
        except:
            return HttpResponse("Page id {0} not found".format(page_id))

    print('No page_id in request')
    return redirect(reverse('index'))

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def user_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            return redirect('index')
        else:
            print(form.errors)
    
    context_dict = {'form': form}

    return render(
        request,
        'rango/profile_registration.html',
        context_dict
    )

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