from django.db import models
from account.models import User
from django.utils.text import slugify


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total = models.FloatField(default=0)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.phone

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ("created_at",)


class OrderItem(models.Model):
    order = models.ForeignKey("cart.Order", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="items")
    size = models.CharField(max_length=12)
    color = models.CharField(max_length=12)
    quantity = models.SmallIntegerField()
    price = models.PositiveSmallIntegerField()


class DiscountCode(models.Model):
    name = models.CharField(max_length=10, unique=True)
    discount = models.SmallIntegerField(default=0)
    quantity = models.SmallIntegerField(default=1)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        super(DiscountCode, self).save()

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کد های تخفیف"
