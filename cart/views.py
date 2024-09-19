
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, DeleteView
from product.models import Product
from cart.cart_module import Cart
from cart.models import Order, OrderItem, DiscountCode
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, "cart/cart_detail.html", {"cart": cart})


class CartAddView(View):
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        size, color, quantity = request.POST.get("size", "empty"), request.POST.get("color", "empty"), request.POST.get(
            "quantity")
        cart = Cart(request)
        cart.add(product, quantity, color, size)
        return redirect("cart:cart_detail")


class CartDeleteView(View):
    def get(self, request, slug):
        cart = Cart(request)
        cart.delete(slug)
        return redirect("cart:cart_detail")


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        return render(request, "cart/order_detail.html", {"order": order})


class OrderCreationView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total=cart.final_total())
        for item in cart:
            OrderItem.objects.create(order=order, product=item["product"], size=item["size"], color=item["color"],
                                     quantity=item["quantity"], price=item["price"])
        cart.remove_cart()

        return redirect("cart:order_detail", order.id)


class DiscountView(LoginRequiredMixin, View):
    def post(self, request, pk):
        code = request.POST.get("discount_code")
        order = get_object_or_404(Order, id=pk)
        discount_code = get_object_or_404(DiscountCode, name=code)
        if discount_code.quantity == 0:
            return redirect("cart:order_detail", order.id)

        order.total -= order.total * discount_code.discount / 100
        order.save()
        discount_code.quantity -= 1
        discount_code.save()

        return redirect("cart:order_detail", order.id)
