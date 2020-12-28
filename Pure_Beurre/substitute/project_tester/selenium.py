from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver as wdc
from selenium.webdriver.opera.webdriver import WebDriver as wdo
from substitute.operations import *
import time


class SeleniumTestsChrome(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.a_text = Text.objects.create(language="fr", mentions_title="test title", mentions_cookies="test content")
        cls.a_user_clear_password = "selenium.1234"
        cls.a_user_chrome = User.objects.create_user(username="chrome_user", email="chrome_user@purebeurre.com", password=cls.a_user_clear_password)
        cls.a_user_chrome.save()
        cls.a_customer_chrome = Customer(user=cls.a_user_chrome)
        cls.a_customer_chrome.save()
        cls.selenium = wdc(executable_path="D:\\STEPHEN_AO\\05_THE_PYTHON_APPLICATION_DEVELOPER\\PROJECTS\\08_Creez_une_plateforme_pour_amateur_de_nutella\\projet\\P8_1.1\\Pure_Beurre\\substitute\\project_tester\\chromedriver.exe")
        cls.selenium.implicitly_wait(10)
        cls.selenium.get('%s%s' % (cls.live_server_url, "/substitute/home/"))

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_logout(self):
        time.sleep(2)
        main_url = self.live_server_url
        self.selenium.find_element_by_class_name("logout").click()
        time.sleep(2)
        self.assertEqual(
            self.selenium.current_url,
            main_url + reverse("substitute:home")
        )

    def test_login(self):
        time.sleep(2)
        main_url = self.live_server_url
        self.selenium.find_element_by_class_name("login").click()
        time.sleep(2)
        self.assertEqual(
            self.selenium.current_url,
            main_url + reverse("substitute:login")
        )
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(self.a_user_chrome.username)
        time.sleep(2)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(self.a_user_clear_password)
        time.sleep(2)
        self.selenium.find_element_by_class_name("connect-user").click()
        time.sleep(2)
        main_url = self.live_server_url
        self.assertEqual(
            self.selenium.current_url,
            main_url + reverse("substitute:account")
        )


class SeleniumTestsOpera(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.a_text = Text.objects.create(language="fr", mentions_title="test title", mentions_cookies="test content")
        cls.a_user_clear_password = "user.1234"
        cls.a_user_opera = User.objects.create_user(username="opera_user", email="opera_user@purebeurre.com", password=cls.a_user_clear_password)
        cls.a_user_opera.save()
        cls.a_customer_opera = Customer(user=cls.a_user_opera)
        cls.a_customer_opera.save()
        cls.selenium = wdo(executable_path="D:\\STEPHEN_AO\\05_THE_PYTHON_APPLICATION_DEVELOPER\\PROJECTS\\08_Creez_une_plateforme_pour_amateur_de_nutella\\projet\\P8_1.1\\Pure_Beurre\\substitute\\project_tester\\operadriver_win64\\operadriver.exe")
        cls.selenium.implicitly_wait(10)
        cls.selenium.get('%s%s' % (cls.live_server_url, "/substitute/home/"))

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

#
    def test_logout(self):
        time.sleep(2)
        main_url = self.live_server_url
        self.selenium.find_element_by_class_name("logout").click()
        time.sleep(2)
        self.assertEqual(
            self.selenium.current_url,
            main_url + reverse("substitute:home")
        )

    def test_login(self):
        time.sleep(2)
        main_url = self.live_server_url
        self.selenium.find_element_by_class_name("login").click()
        time.sleep(2)
        self.assertEqual(
            self.selenium.current_url,
            main_url + reverse("substitute:login")
        )
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(self.a_user_opera.username)
        time.sleep(2)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(self.a_user_clear_password)
        time.sleep(2)
        self.selenium.find_element_by_class_name("connect-user").click()
        time.sleep(2)
        main_url = self.live_server_url
        self.assertEqual(
            self.selenium.current_url,
            main_url + reverse("substitute:account")
        )


class SeleniumTestsError400(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = wdc(executable_path="D:\\STEPHEN_AO\\05_THE_PYTHON_APPLICATION_DEVELOPER\\PROJECTS\\08_Creez_une_plateforme_pour_amateur_de_nutella\\projet\\P8_1.1\\Pure_Beurre\\substitute\\project_tester\\chromedriver.exe")
        cls.selenium.get(cls.live_server_url)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_404(self):
        time.sleep(2)
        alert = self.selenium.find_element_by_id("404-area")
        self.assertEqual(alert.find_element_by_tag_name("h1").text,
                         "Cette page est introuvable !!!!")


class SeleniumTestsError500(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.a_text = Text.objects.create(language="fr", mentions_title="test title", mentions_cookies="test content")
        cls.a_user_clear_password = "error.1234"
        cls.a_user_opera = User.objects.create_user(username="user_error_500", email="user_error_500@purebeurre.com", password=cls.a_user_clear_password)
        cls.a_user_opera.save()
        cls.selenium = wdc(executable_path="D:\\STEPHEN_AO\\05_THE_PYTHON_APPLICATION_DEVELOPER\\PROJECTS\\08_Creez_une_plateforme_pour_amateur_de_nutella\\projet\\P8_1.1\\Pure_Beurre\\substitute\\project_tester\\chromedriver.exe")
        cls.selenium.get('%s%s' % (cls.live_server_url, "/substitute/home/"))

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_500(self):
        time.sleep(2)
        self.selenium.get('%s%s' % (self.live_server_url, "/substitute/home/"))
        time.sleep(2)
        main_url = self.live_server_url
        self.selenium.find_element_by_class_name("login").click()
        time.sleep(2)
        self.assertEqual(
            self.selenium.current_url,
            main_url + reverse("substitute:login")
        )
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(self.a_user_opera.username)
        time.sleep(2)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(self.a_user_clear_password)
        time.sleep(2)
        self.selenium.find_element_by_class_name("connect-user").click()
        time.sleep(2)
        alert = self.selenium.find_element_by_id("500-area")
        self.assertEqual(alert.find_element_by_tag_name("h1").text,
                         "Nous avons un problème interne !!!!")