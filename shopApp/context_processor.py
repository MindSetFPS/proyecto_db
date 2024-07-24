from .models import Category

# https://syscrews.medium.com/context-processor-in-django-62818f14d88f

def my_context_processor(request):
    return {
        'custom' : 'Hello from processor'
    }

def categories(request):
    cats = Category.objects.filter(parent=None)
    return {
        'categories' : cats
    }