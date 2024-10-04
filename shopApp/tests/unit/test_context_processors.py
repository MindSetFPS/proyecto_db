# tests/test_context_processors.py
from django.test import TestCase, RequestFactory
from shopApp.context_processor import my_context_processor, categories, profile_links
from shopApp.models import Category
from shopApp.context_processor import categories, profile_links;

## LISTA
class ContextProcessorTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

    def test_my_context_processor(self):
        context = my_context_processor(self.request)
        self.assertIn('custom', context)
        self.assertEqual(context['custom'], 'Hello from processor')

    def test_categories(self):
        # Assuming you have a Category model with a 'name' field
        Category.objects.create(name="Category 1")
        Category.objects.create(name="Category 2", parent=Category.objects.get(name="Category 1"))

        context = categories(self.request)
        self.assertIn('categories', context)
        self.assertEqual(len(context['categories']), 1)
        self.assertEqual(context['categories'][0].name, "Category 1")

    def test_profile_links(self):
        context = profile_links(self.request)
        self.assertIn('links', context)
        self.assertEqual(len(context['links']), 4)
        self.assertEqual(context['links'][0]['url'], 'profile')
        self.assertEqual(context['links'][1]['url'], 'logout')
        self.assertEqual(context['links'][2]['url'], 'register')
        self.assertEqual(context['links'][3]['url'], 'login')
