from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpRequest
from django.contrib.auth import authenticate, login, logout
# from .forms import UserRegistrationForm, LoginForm
from shopApp.forms import UserRegistrationForm, LoginForm
from django.contrib.admin.views.decorators import staff_member_required
# from .models import Product, ShoppingCart, Order, OrderDetail, Category, Image, Customer
from shopApp.models import Product, ShoppingCart, Category, Image, Customer

def create_category_list(product: Product):
    categories = []
    category = product.category

    while(category):
        categories.append(category.name)
        category = category.parent

    return categories

# Create your views here.
@staff_member_required
def my_custom_viewer(request):
    context = {
        'title': 'my custom admin page'
    }
    return render(request, 'admin/my_custom_template.html', context)

def index(request):
    # Get products
    product_list = Product.objects.filter(stock__gt=0)
    
    # Get products images
    for product in product_list:
        image = Image.objects.filter(product=product).first()
        if image:
            product.image_url = image.image_url  
        else:
            product.image_url = None  

    return render(request, 'home.html', {'productos': product_list})

def product(request, product_id):
    try:
        get_product = Product.objects.get(pk=product_id)
        images = Image.objects.filter(product=get_product)
        categories = create_category_list(product=get_product)
        categories = list(reversed(categories))
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    return render(request, "product.html", {"product": get_product, "images": images, "product_categories": categories})

def register(request: HttpRequest):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cart_items = ShoppingCart.objects.filter(session_id=request.session.session_key)

            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            # Log the user in and redirect to homepage
            user = authenticate(username=new_user.username,password=form.cleaned_data['password'])
            Customer.objects.create(user=user)

            for item in cart_items:
                item.user = new_user
                item.save()

            login(request, user)

            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request: HttpRequest):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                print('ola')

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def remove_product_cart(request: HttpRequest, product_id):
    if request.POST:
        if request.user.is_authenticated:
            # product = get_object_or_404(Product, id=product_id)
            cart_item = ShoppingCart.objects.filter(user=request.user, product_id=str(product_id))
            cart_item.delete()
            print(cart_item)
        else:
            cart_item = ShoppingCart.objects.filter(session_id=request.session.session_key, product_id=str(product_id))
            cart_item.delete()
    return redirect('view_cart')

def add_to_cart(request: HttpRequest, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':

        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        if request.user.is_authenticated:
            cart_item, created = ShoppingCart.objects.get_or_create(user=request.user, product_id=str(product.id))
        else:
            cart_item, created = ShoppingCart.objects.get_or_create(session_id=session_id, product_id=str(product.id))

        if product.stock > cart_item.amount:
            cart_item.amount += 1
            cart_item.save()
        return redirect('view_cart')

# Badcode, probably
def decrease_cart_product(request: HttpRequest, product_id):
    if request.POST:
        if request.user.is_authenticated:
            cart_item = ShoppingCart.objects.filter(user=request.user, product_id=str(product_id)).first()
            if cart_item.amount - 1 < 1:
                cart_item.delete()
            else:
                cart_item.amount = cart_item.amount - 1
                cart_item.save()
        else:
            cart_item = ShoppingCart.objects.filter(session_id=request.session.session_key, product_id=str(product_id)).first()
            if cart_item.amount - 1 < 1:
                cart_item.delete()
            else:
                cart_item.amount = cart_item.amount - 1
                cart_item.save()

    return redirect('view_cart')

def view_cart(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    if session_id is None:
        return HttpResponse("Session ID is None")

    try:
        if request.user.is_authenticated:
            cart_items = ShoppingCart.objects.filter(user=request.user)
        else:
            cart_items = ShoppingCart.objects.filter(session_id=session_id)

    except Exception as e:
        return HttpResponse(f"Error: {e}")

    products = []
    total_price = 0
    item_count = 0

    for item in cart_items:
        prod = Product.objects.get(id=item.product_id)
        prod_data = {
            'name': prod.name,
            'price': prod.price,
            'amount': item.amount,
            'id': item.product_id,
            'image_url': Image.image_url,
            'total': prod.price * item.amount
        }

        products.append(prod_data)
        total_price = total_price + (prod.price * item.amount)
        item_count = item_count + item.amount

    return render(request, 'shoppingcar.html', {'cart_items': cart_items, 'products': products, 'total_price': total_price, 'item_count': item_count})

def category(request, category):
    if len(category) == 0:
        # Link to all categories
        return render(request, 'categories.html')
    else:
        cat = Category.objects.filter(name=category).first()
        products = Product.objects.filter(category=cat.id)
        
        for product in products:
            image = Image.objects.filter(product=product).first()
            product.image_url = image.image_url

        return render(request, 'category.html', {'products': products, 'category': cat.name})
