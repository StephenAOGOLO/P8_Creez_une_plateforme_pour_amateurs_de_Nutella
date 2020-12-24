""" This module test the whole project """
from . import views
from .models import *
#from .operations import DataSearch, DataAliment, DataSave, Data
from .operations import *
#from .management.commands import fillDB
from django.conf.urls import handler404, handler500
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase, SimpleTestCase, Client


# Create your tests here.


class TestViewsUnlogged(TestCase):
    """ This test class is launched to verify the front-end components when user is not logged """
    def setUp(self):
        """ This method prepares the initial test environment.
        It creates the following instances :
            - Aliments
            - Users
            - Customers
        Every urls are reversed to check their attached function."""
        self.c = Client()
        self.an_aliment = Aliment.objects.create(name="an_aliment")
        self.another_aliment = Aliment.objects.create(name="another_aliment")
        self.a_user = User.objects.create_user(username="a_user", email="a_user@purebeurre.com", password="user.1234")
        self.a_second_user = User.objects.create_user(username="a_second_user", email="a__second_user@purebeurre.com", password="a_second_user.1234")
        self.a_customer = Customer(user=self.a_user)
        self.a_customer.save()
        self.error_404_url = handler404
        self.error_500_url = handler500
        self.home_url = reverse("substitute:home")
        self.historic_url = reverse("substitute:historic")
        self.register_url = reverse("substitute:register")
        self.account_url = reverse("substitute:account")
        self.login_url = reverse("substitute:login")
        self.logout_url = reverse("substitute:logout")
        self.search_url = reverse("substitute:search", args=["an_aliment"])
        self.aliment_url = reverse("substitute:aliment", args=[self.an_aliment.id, self.another_aliment.id, self.a_user.id])
        self.save_url = reverse("substitute:save", args=[self.an_aliment.id, self.another_aliment.id, self.a_user.id])
        self.an_object = True
        self.another_object = False

    def test_0_setUp(self):
        """ This method is a generic test. """
        self.assertEqual("a", "a")

    def test_1_setUp(self):
        """ This method is a generic test. """
        self.assertEqual(self.an_object, True)
        self.assertEqual(self.another_object, False)

    def test_2_index_setUp(self):
        """ This method tests if '/substitute/' works. """
        response = self.c.post("/substitute/")
        result = response.status_code
        self.assertEqual(result, 200)

    def test_3_home_setUp(self):
        """ This method tests if '/substitute/home/' works. """
        response = self.c.post("/substitute/home/")
        result = response.status_code
        self.assertEqual(result, 200)

    def test_search_view_2(self):
        """ This method tests the redirection after searching a product. """
        print("\n\ntest_search_view_2")
        response = self.c.get("/substitute/search/product=pizza", follow=True)
        print(response.redirect_chain)
        result = response.status_code
        print(result)
        self.assertEqual(result, 200)

    def test_aliment_view_1(self):
        """ This method tests if the reversed 'aliment' url works. """
        print("\n\ntest_aliment_view_1")
        response = self.c.get(self.aliment_url)
        result = response.status_code
        print(result)
        self.assertEqual(result, 200)

    def test_save_view_1(self):
        """ This method tests if the reversed 'save' url works. """
        print("\n\ntest_save_view_1")
        response = self.c.get(self.save_url)
        result = response.status_code
        print(result)
        self.assertEqual(result, 200)


    def test_login_view_1(self):
        """ This method tests if '/substitute/login/' works. """
        print("\n\ntest_login_view_1")
        response = self.c.get("/substitute/login/")
        result = response.status_code
        self.assertEqual(result, 200)

    def test_register_view_1(self):
        """ This method tests if '/substitute/register/' works. """
        print("\n\ntest_register_view_1")
        response = self.c.get("/substitute/register/")
        result = response.status_code
        self.assertEqual(result, 200)

    def test_logout_view_1(self):
        """ This method tests the redirection after logging out. """
        print("\n\ntest_logout_view_1")
        response = self.c.get("/substitute/logout/", follow=True)
        print(response.redirect_chain)
        result = response.status_code
        print(result)
        self.assertEqual(result, 200)

    def test_home_html(self):
        """ This method tests if the reversed 'home' url works. """
        print("\n\ntest_home_html")
        response = self.c.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "substitute/home.html")

    def test_search_html(self):
        """ This method check if 'home.html' is used. """
        print("\n\ntest_search_html")
        response = self.c.get(self.search_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "substitute/home.html")


    def test_aliment_html(self):
        """ This method check if 'aliment.html' is used. """
        print("\n\ntest_aliment_html")
        response = self.c.get(self.aliment_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "substitute/aliment.html")

    def test_save_html(self):
        """ This method check if 'save.html' is used. """
        print("\n\ntest_save_html")
        response = self.c.get(self.aliment_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "substitute/save.html")


    def test_register_html(self):
        """ This method check if 'register.html' is used. """
        print("\n\ntest_register_html")
        response = self.c.get(self.register_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_login_html(self):
        """ This method check if 'login.html' is used. """
        print("\n\ntest_login_html")
        response = self.c.get(self.login_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")


    def test_logout_html(self):
        """ This method check if 'home.html' is used. """
        print("\n\ntest_logout_html")
        response = self.c.get(self.logout_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "substitute/home.html")

    def test_search_POST(self):
        """ This method check the redirection when 'search' url is used. """
        print("\n\ntest_search_POST")
        response = self.c.post(self.search_url)
        print(response)
        self.assertEqual(response.status_code, 302)

    def test_aliment_POST(self):
        """ This method check if 'aliment' url works. """
        print("\n\ntest_aliment_POST")
        response = self.c.post(self.aliment_url)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_save_POST(self):
        """ This method check if 'save' url works. """
        print("\n\ntest_save_POST")
        response = self.c.post(self.save_url)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_register_POST(self):
        """ This method check if 'register' url works. """
        print("\n\ntest_register_POST")
        response = self.c.post(self.register_url)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_login_POST(self):
        """ This method check if 'login' url works. """
        print("\n\ntest_login_POST")
        a_user = {"id": self.a_user.id,
                  "username": self.a_user.username,
                  "email": self.a_user.email,
                  "password": self.a_user.password}
        response = self.c.post(self.login_url, a_user)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_logout_POST(self):
        """ This method check if 'login' url works. """
        print("\n\ntest_logout_POST")
        response = self.c.post(self.login_url)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_404(self):
        """ This method check if 'error404' url works. """
        print("\n\ntest_404")
        response = self.c.post("/substitute/home/error404")
        print(response)
        self.assertEqual(response.status_code, 404)

    def test_404_html(self):
        """ This method check if '404.html' is used. """
        print("\n\ntest_404_html")
        response = self.c.get(self.error_404_url, follow=True)
        self.assertTemplateUsed(response, "errors/404.html")


class TestViewsLogged(TestCase):
    """ This test class is launched to verify the front-end components when user is logged """
    def setUp(self):
        """ This method prepares the initial test environment.
        It creates the following instances :
            - Aliments
            - Users
            - Customers
        Every urls are reversed to check their attached function."""
        self.c = Client()
        self.an_aliment = Aliment.objects.create(name="an_aliment")
        self.another_aliment = Aliment.objects.create(name="another_aliment")
        self.a_user = User.objects.create_user(username="a_user", email="a_user@purebeurre.com", password="user.1234")
        self.a_second_user = User.objects.create_user(username="a_second_user", email="a__second_user@purebeurre.com", password="a_second_user.1234")
        self.a_customer = Customer(user=self.a_user)
        self.a_customer.save()
        self.c.login(username="a_user", password="user.1234")
        self.browser_product = {"browser_product": "browser_product"}
        self.index_url = reverse("substitute:index")
        self.error_404_url = handler404
        self.error_500_url = handler500
        self.home_url = reverse("substitute:home")
        self.historic_url = reverse("substitute:historic")
        self.register_url = reverse("substitute:register")
        self.account_url = reverse("substitute:account")
        self.login_url = reverse("substitute:login")
        self.search_url = reverse("substitute:search", args=["an_aliment"])
        self.aliment_url = reverse("substitute:aliment", args=[self.an_aliment.id, self.another_aliment.id, self.a_user.id])
        self.save_url = reverse("substitute:save", args=[self.an_aliment.id, self.another_aliment.id, self.a_user.id])
        self.an_object = True
        self.another_object = False

    def test_0_setUp(self):
        """ This method is a generic test. """
        self.assertEqual("a", "a")

    def test_1_setUp(self):
        """ This method is a generic test. """
        self.assertEqual(self.an_object, True)
        self.assertEqual(self.another_object, False)

    def test_2_index_setUp(self):
        """ This method tests if '/substitute/' works. """
        response = self.c.post("/substitute/")
        result = response.status_code
        self.assertEqual(result, 200)

    def test_3_home_setUp(self):
        """ This method tests if '/substitute/home/' works. """
        response = self.c.post("/substitute/home/")
        result = response.status_code
        self.assertEqual(result, 200)

    def test_404(self):
        """ This method tests if 'error404' works. """
        print("\n\ntest_404")
        response = self.c.post("/substitute/home/error404")
        print(response)
        self.assertEqual(response.status_code, 404)

    def test_404_html(self):
        """ This method checks if '404.html' is used. """
        print("\n\ntest_404_html")
        response = self.c.get(self.error_404_url, follow=True)
        self.assertTemplateUsed(response, "errors/404.html")

    def test_index_view(self):
        """ This method tests if 'index' url works. """
        print("\n\ntest_search_view_2")
        response = self.c.get(self.index_url)
        result = response.status_code
        print(result)
        self.assertEqual(result, 200)

    def test_search_view_2(self):
        """ This method tests the redirection after searching a product. """
        print("\n\ntest_search_view_2")
        response = self.c.get("/substitute/search/product=pizza", follow=True)
        print(response.redirect_chain)
        result = response.status_code
        print(result)
        self.assertEqual(result, 200)

    def test_aliment_view_1(self):
        """ This method tests if 'aliment' url works. """
        print("\n\ntest_aliment_view_1")
        response = self.c.get(self.aliment_url)
        result = response.status_code
        print(result)
        self.assertEqual(result, 200)

    def test_save_view_1(self):
        """ This method tests if 'save' url works. """
        print("\n\ntest_save_view_1")
        response = self.c.get(self.save_url)
        result = response.status_code
        print(result)
        self.assertEqual(result, 200)

    def test_historic_view_1(self):
        """ This method tests if 'historic' url works. """
        print("\n\ntest_historic_view_1")
        response = self.c.get(self.historic_url)
        result = response.status_code
        self.assertEqual(result, 200)

    def test_account_view_1(self):
        """ This method tests if 'account' url works. """
        print("\n\ntest_account_view_1")
        response = self.c.get(self.account_url)
        result = response.status_code
        self.assertEqual(result, 200)

    def test_login_view_1(self):
        """ This method tests if the redirection works after '/substitute/login/'  """
        print("\n\ntest_login_view_1")
        response = self.c.get("/substitute/login/")
        result = response.status_code
        self.assertEqual(result, 302)

    def test_register_view_1(self):
        """ This method tests if the redirection works after '/substitute/register/'  """
        print("\n\ntest_register_view_1")
        response = self.c.get("/substitute/register/")
        result = response.status_code
        self.assertEqual(result, 302)

    def test_logout_view_1(self):
        """ This method tests if the redirection works after '/substitute/logout/'  """
        print("\n\ntest_logout_view_1")
        response = self.c.get("/substitute/logout/", follow=True)
        print(response.redirect_chain)
        result = response.status_code
        print(result)
        self.assertEqual(result, 200)

    def test_home_html(self):
        """ This method tests if 'home.html' is used.  """
        print("\n\ntest_home_html")
        response = self.c.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "substitute/home.html")

    def test_search_html(self):
        """ This method tests if 'home.html' is used. """
        print("\n\ntest_search_html")
        response = self.c.get(self.search_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "substitute/home.html")

    def test_aliment_html(self):
        """ This method tests if 'aliment.html' is used. """
        print("\n\ntest_aliment_html")
        response = self.c.get(self.aliment_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "substitute/aliment.html")

    def test_save_html(self):
        """ This method tests if 'save.html' is used. """
        print("\n\ntest_save_html")
        response = self.c.get(self.aliment_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "substitute/save.html")

    def test_historic_html(self):
        """ This method tests if 'historic.html' is used. """
        print("\n\ntest_historic_html")
        response = self.c.get(self.historic_url)
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "substitute/historic.html")

    def test_account_html(self):
        """ This method tests if 'account.html' is used. """
        print("\n\ntest_account_html")
        print(resolve(self.account_url))
        response = self.c.get(self.account_url)
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "substitute/account.html")

    def test_home_POST(self):
        """ This method tests if 'home' url works. """
        print("\n\ntest_home_POST")
        response = self.c.post(self.home_url)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_home_POST_product(self):
        """ This method tests if the redirection works after search a product. """
        print("\n\ntest_home_POST")
        product = {"product": "product"}
        response = self.c.post(self.home_url, product)
        print(response)
        self.assertEqual(response.status_code, 302)

    def test_home_POST_browser_product(self):
        """ This method tests if the redirection works after search a product on browser. """
        print("\n\ntest_home_POST_browser_product")
        response = self.c.post(self.home_url, self.browser_product)
        print(response)
        self.assertEqual(response.status_code, 302)

    def test_home_POST_product_empty(self):
        """ This method tests if 'home' url works after search an empty product"""
        print("\n\ntest_home_POST_product_empty")
        product = {"product": ""}
        response = self.c.post(self.home_url, product)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_search_POST(self):
        """ This method tests if redirection works after 'search' url. """
        print("\n\ntest_search_POST")
        response = self.c.post(self.search_url)
        print(response)
        self.assertEqual(response.status_code, 302)

    def test_search_POST_browser_product(self):
        """ This method tests if the redirection works after search a product on browser """
        print("\n\ntest_search_POST_browser_product")
        response = self.c.post(self.search_url, self.browser_product)
        print(response)
        self.assertEqual(response.status_code, 302)

    def test_aliment_POST(self):
        """ This method tests if 'aliment' url works. """
        print("\n\ntest_aliment_POST")
        response = self.c.post(self.aliment_url)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_aliment_POST_browser_product(self):
        """ This method tests if 'aliment' url works after search product on browser. """
        print("\n\ntest_aliment_POST_browser_product")
        response = self.c.post(self.aliment_url, self.browser_product)
        print(response)
        self.assertEqual(response.status_code, 302)

    def test_save_POST(self):
        """ This method tests if 'save' url works """
        print("\n\ntest_save_POST")
        response = self.c.post(self.save_url)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_save_POST_browser_product(self):
        """ This method tests if 'save' url works after search product on browser. """
        print("\n\ntest_save_POST_browser_product")
        response = self.c.post(self.save_url, self.browser_product)
        print(response)
        self.assertEqual(response.status_code, 302)

    def test_register_POST(self):
        """ This method tests if the redirection works after 'register' url. """
        print("\n\ntest_register_POST")
        response = self.c.post(self.register_url)
        print(response)
        self.assertEqual(response.status_code, 302)

    def test_register_POST_browser_product(self):
        """ This method tests if 'register' url works after search product on browser. """
        print("\n\ntest_register_POST_browser_product")
        response = self.c.post(self.register_url)
        print(response)
        self.assertEqual(response.status_code, 302)

    def test_login_POST(self):
        """ This method tests if the redirection works after 'login' url. """
        print("\n\ntest_login_POST")
        a_user = {"id": self.a_user.id, "username": self.a_user.username, "email":self.a_user.email, "password": self.a_user.password}
        response = self.c.post(self.login_url, a_user)
        print(response)
        self.assertEqual(response.status_code, 302)

    def test_login_POST_browser_product(self):
        """ This method tests if 'login' url works after search product on browser. """
        print("\n\ntest_login_POST_browser_product")
        response = self.c.post(self.login_url, self.browser_product)
        print(response)
        self.assertEqual(response.status_code, 302)


    def test_historic_POST(self):
        """ This method tests if 'historic' url works. """
        print("\n\ntest_historic_POST")
        response = self.c.post(self.historic_url)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_historic_POST_browser_product(self):
        """ This method tests if 'historic' url works after search product on browser. """
        print("\n\ntest_historic_POST_browser_product")
        response = self.c.post(self.historic_url, self.browser_product)
        print(response)
        self.assertEqual(response.status_code, 302)

    def test_account_POST(self):
        """ This method tests if 'account' url works. """
        print("\n\ntest_account_POST")
        response = self.c.post(self.account_url)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_account_POST_browser_product(self):
        """ This method tests if 'account' url works after search product on browser. """
        print("\n\ntest_account_POST_browser_product")
        response = self.c.post(self.account_url, self.browser_product)
        print(response)
        self.assertEqual(response.status_code, 302)


class TestUrls(SimpleTestCase):
    """ This test class is especially launched to verify the urls. """
    def setUp(self):
        """ This method prepares the initial test environment.
        It creates the following instances :
            - Aliments
            - Users
            - Customers
        'home' and 'search' urls are reversed to check their attached function."""
        self.c = Client()
        self.an_aliment = "an_aliment"
        self.another_aliment = "another_aliment"
        self.a_user = "a_user"
        self.a_customer = "a_customer"
        self.home_url = reverse("substitute:home")
        self.search_url = reverse("substitute:search", args=[self.an_aliment])

    def test_url_home(self):
        """ This method checks if the relation between the 'home' url and its function is insured. """
        print("\n\ntest_url_home")
        url = resolve("/substitute/home/")
        rev = reverse("substitute:home")
        print(url)
        print(rev)
        self.assertEqual(url.func, views.homepage)
        self.assertEqual(rev, self.home_url)
        self.assertEqual(rev, "/" + url.route)

    def test_url_search(self):
        """ This method checks if the relation between the 'search' url and its function is insured. """
        print("\n\ntest_url_search")
        url = resolve("/substitute/search/product=an_aliment")
        rev = reverse("substitute:search", args=[self.an_aliment])
        print(url)
        print(rev)
        self.assertEqual(resolve(rev).func, views.search)
        self.assertEqual(rev, self.search_url)


class TestModels(TestCase):
    """ This test class is launched to verify the back-end components. It takes care of the database. """
    def setUp(self):
        """ This method prepares the initial test environment.
        It creates the following instances (Test model is excluded):
            - Aliments
            - Category
            - Users
            - Customers
        Main urls are reversed to check their attached function.
        """
        self.c = Client()
        self.a_category = Category.objects.create(name="a_category")
        self.another_category = Category.objects.create(name="another_category")
        self.an_aliment = Aliment.objects.create(name="an_aliment")
        self.another_aliment = Aliment.objects.create(name="another_aliment")
        self.a_user = User.objects.create_user("a_user")
        self.a_customer = Customer(user_id=self.a_user.id)
        self.a_customer.save()
        self.home_url = reverse("substitute:home")
        self.historic_url = reverse("substitute:historic")
        self.account_url = reverse("substitute:account")
        self.search_url = reverse("substitute:search", args=["an_aliment"])
        self.aliment_url = reverse("substitute:aliment", args=[self.an_aliment.id, self.another_aliment.id, self.a_user.id])
        self.save_url = reverse("substitute:save", args=[self.an_aliment.id, self.another_aliment.id, self.a_customer.id])

    def test_category_db(self):
        """ This method checks if a category has been correctly save in the database.  """
        index = ["first", "second", "third"]
        for i, e in enumerate(index):
            a_aliment = Aliment.objects.create(name=e, category=self.a_category)
            another_aliment = Aliment.objects.create(name=e, category=self.another_category)
            print(a_aliment.name, a_aliment.category)
            print(another_aliment.name, another_aliment.category)
        all_categories = Category.objects.all()
        category_number = len(all_categories)
        all_aliments = Aliment.objects.all()
        aliment_number = len(all_aliments)
        self.assertEqual((len(index) * category_number) + 2, aliment_number)
        self.assertEqual(category_number, 2)

    def test_customer_model_db(self):
        """ This method checks if a customer has been correctly save in the database.  """
        size_before = len(Customer.objects.all())
        self.a_local_user = User.objects.create_user("a_local_user")
        self.a_local_customer = Customer(user_id=self.a_local_user.id)
        self.a_local_customer.save()
        size_after = len(Customer.objects.all())
        self.assertEqual(size_after, size_before + 1)

    def test_historic_model_db(self):
        """ This method checks if a historic's record has been correctly save in the database.  """
        index = ["first", "second", "third"]
        size_before = len(Historic.objects.all())
        for i, e in enumerate(index):
            a_aliment = Aliment.objects.create(name=e, category=self.a_category)
            a_record = Historic.objects.create(user=self.a_customer, aliment=self.an_aliment, substitute=self.another_aliment)
            print(a_aliment)
            print(a_record)
        size_after = len(Historic.objects.all())
        self.assertEqual(size_before, 0)
        self.assertEqual(size_after, 3)


class TestOperations(TestCase):
    """ This test class is launched to verify the back-end components. It takes care of the operations module. """
    def setUp(self):
        """ This method prepares the initial test environment.
        It creates the following instances (Test model is excluded):
            - Aliments
            - Category
            - Users
            - Customers
        Main urls are reversed to check their attached function.
        """
        self.c = Client()
        self.a_user = User.objects.create_user(username="a_user", email="a_user@purebeurre.com", password="user.1234")
        self.a_customer = Customer(user=self.a_user)
        self.a_customer.save()
        self.c.login(username="a_user", password="user.1234")
        self.a_category = Category.objects.create(id_name="a_category", name="a_category")
        self.an_aliment = Aliment.objects.create(name="an_aliment", category=self.a_category.name)
        self.an_aliment.tag.add(self.a_category)
        self.text = "text"

    def test_DataSearch(self):
        """ This method checks if no product is return when a unknown product has been seized. """
        result = DataSearch(self.text)
        data = result.big_data
        print(data)
        self.assertEqual(data, {})

    def test_DataSearch_direct_aliment(self):
        """ This method checks if direct products is return when a known product has been seized. """
        result = DataSearch(self.an_aliment.name)
        data = result.big_data
        print(data)
        self.assertEqual(data, {self.an_aliment.id: self.an_aliment})

    def test_DataSearch_indirect_aliment(self):
        """ This method checks if indirect products is return when a known product has been seized. """
        print(self.an_aliment.category)
        result = DataSearch(self.a_category.name)
        print("-")
        data = result.big_data
        print(data)
        self.assertEqual(data, {self.an_aliment.id: self.an_aliment})

    def test_DataAliment(self):
        """ This method checks if a product is return when a correct id product has been seized. """
        result = DataAliment(self.an_aliment.id)
        data = result.aliment
        print(data)
        self.assertEqual(data, self.an_aliment)

    def test_DataSave(self):
        """ This method checks if a historic record has been corectly stored. """
        size_before = len(Historic.objects.all())
        another_aliment = Aliment.objects.create(name="another_aliment")
        record = DataSave(self.an_aliment, another_aliment, self.a_customer)
        record.store_data()
        size_after = len(Historic.objects.all())
        self.assertEqual(size_after, size_before + 1)


    def test_Data(self):
        """ This method tests if products and categories have been correctly stored. """
        result = Data(".\\substitute\\static\\substitute\\json\\min_urls.json")
        size_aliment_before = len(Aliment.objects.all())
        size_category_before = len(Category.objects.all())
        data = result.big_data
        print(data)
        fill_category(data)
        fill_aliment(data)
        size_aliment_after = len(Aliment.objects.all())
        size_category_after = len(Category.objects.all())
        print(size_aliment_after)
        print(size_category_after)
        self.assertGreater(size_aliment_after, size_aliment_before)
        self.assertGreater(size_category_after, size_category_before)

    def test_get_historic(self):
        """ This method checks if a historic record is correctly found and returned thanks to a given customer. """
        the_historic = get_historic(self.a_customer)
        self.assertEqual(len(the_historic), 0)
        another_aliment = Aliment.objects.create(name="another_aliment")
        record = DataSave(self.an_aliment, another_aliment, self.a_customer)
        record.store_data()
        the_historic = get_historic(self.a_customer)
        self.assertEqual(len(the_historic), 1)
