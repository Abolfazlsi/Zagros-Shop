from product.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")

        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            product = Product.objects.get(slug=str(item["id"]))
            item["product"] = product
            item["total"] = float(item["quantity"]) * float(item["price"])
            item["unique_id"] = self.unique_id_generator(product.slug, item["color"], item["size"])

            yield item

    def unique_id_generator(self, slug, color, size):
        result = f"{slug}-{color}-{size}"
        return result

    def add(self, product, quantity, color, size):
        unique = self.unique_id_generator(product.slug, color, size)
        if unique not in self.cart:
            self.cart[unique] = {"quantity": 0, "price": str(product.price), "color": color, "size": size,
                                 "id": str(product.slug)}

        self.cart[unique]["quantity"] += int(quantity)
        self.save()

    def remove_cart(self):
        del self.session["cart"]

    def final_total(self):
        cart = self.cart.values()
        total = sum(float(item["price"]) * float(item["quantity"]) for item in cart)
        return total

    def delete(self, slug):
        if slug in self.cart:
            del self.cart[slug]
            self.save()

    def save(self):
        self.session.modified = True
