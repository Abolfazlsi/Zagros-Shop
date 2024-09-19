from product.models import Product, Category, Size, Color
from cart.cart_module import Cart


def products(request):
    products_list = Product.objects.all()

    return {"products_list": products_list}


def recent_products(request):
    recent_product = Product.objects.all().order_by("-created")

    return {"recent_product": recent_product}


def categories(request):
    category = Category.objects.all()

    return {"categories": category}


def cart_detail(request):
    cart = Cart(request)

    return {"cart": cart}
