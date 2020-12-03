from django.test import TestCase

# Create your tests here.

class IndexPageTestCase(TestCase):
    def test_index_page(self):
        self.assertEqual("a", "a")