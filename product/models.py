from django.db import models
from django.core import validators
from django.urls import reverse
from django.utils.text import slugify
from account.models import User


class Size(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        verbose_name = "اندازه"
        verbose_name_plural = "اندازه"

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=15)

    class Meta:
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ ها"

    def __str__(self):
        return self.name


class Category(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="subs")
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product:category_detail", args=[self.slug])


class Information(models.Model):
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="informations", null=True)
    text = models.TextField()

    def __str__(self):
        return self.text[:30]

    class Meta:
        verbose_name = "اطلاعات"
        verbose_name_plural = "اطلاعات"


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.SmallIntegerField()
    discount = models.SmallIntegerField()
    image = models.ImageField(upload_to="products")
    size = models.ManyToManyField("product.Size", related_name="products", blank=True, null=True)
    color = models.ManyToManyField("product.Color", related_name="products")
    category = models.ManyToManyField("product.Category", related_name="products", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product:product_detail", args=[self.slug])

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super(Product, self).save()


class ContactUs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contactus")
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.user} - {self.message[:30]}"

    class Meta:
        verbose_name = "تماس با ما"
        verbose_name_plural = "تماس با ما"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="comments", null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.text[:30]}"

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

        ordering = ("-created_at",)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="ratings")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product}"

    class Meta:
        verbose_name = "امتیاز"
        verbose_name_plural = "امتیاز ها"
        ordering = ("-created_at",)


class SaveProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saves")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="saves")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user} - {self.product.title}"
