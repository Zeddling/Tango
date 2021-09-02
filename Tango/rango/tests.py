from django.contrib.auth.models import User
from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.staticfiles import finders


class AboutPageTests(TestCase):
    def test_about_using_template(self):
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'rango/about.html')

    def test_about_contains_create_message(self):
        response = self.client.get(reverse('about'))
        self.assertIn(b'This tutorial has been put together by', response.content)

    def test_about_contain_image(self):
        response = self.client.get(reverse('about'))
        self.assertIn(b'img src="/media/', response.content)
    
    def test_sessionid_cookie_is_set(self):
        response = self.client.get(reverse('about'))
        self.assertIn('sessionid', response.client.cookies)


class AdminPageTests(TestCase):

    def test_admin_interface_page_view(self):
        from rango.admin import PageAdmin
        self.assertIn('category', PageAdmin.list_display)
        self.assertIn('url', PageAdmin.list_display)


class CategoryFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="12345")
        self.user.save()
        self.client.login(username="test", password="12345")
    
    def tearDown(self):
        self.client.logout()
        self.user.delete()
    
    def test_link_to_category_form_in_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertIn(b'<a href="/rango/category/add_category"', response.content)

    def test_add_category_template_used(self):
        response = self.client.get(reverse('add_category'))
        self.assertTemplateUsed(response, 'rango/add_category.html')
    
    def test_form_is_generated(self): 
        response = self.client.get(reverse('add_category'))
        self.assertIn(b'<label', response.content)


class CategoryPageTests(TestCase):
    def setUp(self):
        try:
            from populate_rango import populate
            populate()
        except ImportError:
            print('The module populate_rango does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function :-(')
    
    def test_category_page_exists(self):
        response = self.client.get(reverse('show_category', args=['python']))
        self.assertTemplateUsed(response, 'rango/category.html')


class GeneralTests(TestCase):
    def test_serving_static_files(self):
        result = finders.find('images/rango.jpg')
        self.assertIsNotNone(result)


class IndexPageTests(TestCase):
    def setUp(self):
        try:
            from populate_rango import populate
            populate()
        except ImportError:
            print('The module populate_rango does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function :-(')

    def test_index_contains_hello_message(self):
        response = self.client.get(reverse('index'))
        self.assertIn(b'Rango says', response.content)

    def test_index_using_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'rango/index.html')

    def test_rango_picture_displayed(self):
        response = self.client.get(reverse('index'))
        self.assertIn(b'<img src="/static/images/rango.jpg"', response.content)

    def test_index_has_title(self):
        response = self.client.get(reverse('index'))
        self.assertIn(b'<title>', response.content)
        self.assertIn(b'</title>', response.content)

    #   Test that categories list is created
    def test_index_has_categories_displayed(self):
        response = self.client.get(reverse('index'))
        self.assertIn(b'<ul', response.content)
        self.assertIn(b'</ul>', response.content)

    def test_categorical_urls_generated(self):
        response = self.client.get(reverse('index'))
        self.assertIn(b'<a href="/rango/category/', response.content)
    
    def test_most_liked_and_most_viewed(self):
        response = self.client.get(reverse('index'))
        self.assertIn(b'Most Liked Categories', response.content)
        self.assertIn(b'Most Viewed Pages', response.content)


class ModelTests(TestCase):
    def setUp(self):
        try:
            from populate_rango import populate
            populate()
        except ImportError:
            print('The module populate_rango does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function :-(')
    
    def get_category(self, name):
        from rango.models import Category
        try:
            category = Category.objects.get(name=name)
        except Category.DoesNotExist:
            category = None
        return category
    
    def test_python_category_added(self):
        category = self.get_category('Python')
        self.assertIsNotNone(category)
    
    def test_python_category_with_views(self):
        category = self.get_category('Python')
        self.assertEquals(category.views, 128)

    def test_python_category_with_likes(self):
        category = self.get_category('Python')
        self.assertEquals(category.likes, 64)
    
    def test_does_slug_field_work(self):
        from rango.models import Category
        category = Category(name="how do I create a slug in django")
        category.save()
        self.assertEqual(category.slug, 'how-do-i-create-a-slug-in-django')
    
    def test_slug_field_not_null(self):
        category = self.get_category('Python')
        self.assertIsNotNone(category.slug)


class PageFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="12345")
        self.user.save()
        self.client.login(username="test", password="12345")
    
    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def test_add_page_exists(self):
        response = self.client.get(reverse('add_page', args=['python']))
        self.assertTemplateUsed(response, 'rango/add_page.html')

    def test_assert_form_is_generated(self):
        response = self.client.get(reverse('add_page', args=['python']))
        self.assertIn(b'<label', response.content)

class UserProfileFormTests(TestCase):
    def test_user_profile_form_page_exists(self):
        response = self.client.get(reverse('register_profile'))
        self.assertTemplateUsed(response, 'rango/profile_registration.html')

class UserProfilePageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="12345")
        self.user.save()
        self.client.login(username="test", password="12345")
    
    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def test_user_profile_page_exists(self):
        response = self.client.get(reverse('profile', args=['test']))
        self.assertTemplateUsed(response, 'rango/profile.html')
