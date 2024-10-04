from .models import Category

# https://syscrews.medium.com/context-processor-in-django-62818f14d88f

def my_context_processor(request):
    return {
        'custom': 'Hello from processor'
    }

def categories(request):
    cats = Category.objects.filter(parent=None)
    return {
        'categories': cats
    }

def profile_links(request):
    return {'links': [
        {"loggedin_required": True, "url": "profile", "name": "Profile", "icon": "icons/user.html"},
        {"loggedin_required": True, "url": "logout", "name": "Logout", "icon": "icons/exit.html"},
        {"loggedin_required": False, "url": "register", "name": "Register", "icon": "icons/user.html"},
        {"loggedin_required": False, "url": "login", "name": "Login", "icon": ""}
    ]}
