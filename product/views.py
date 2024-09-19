from django.shortcuts import render, reverse, redirect, get_object_or_404, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView, FormView, View, CreateView
from product.models import Product, Color, Category, ContactUs, Comment, Rating, SaveProduct
from product.forms import ContactUsForm, CommentForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductView(ListView):
    paginate_by = 9
    model = Product
    template_name = "product/products_list.html"

    def get_context_data(self, **kwargs):
        request = self.request
        colors = request.GET.getlist("color")
        sizes = request.GET.getlist("size")
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        queryset = Product.objects.all()
        if colors:
            queryset = queryset.filter(color__name__in=colors).distinct()

        if sizes:
            queryset = queryset.filter(size__name__in=sizes).distinct()

        if max_price and min_price:
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price).distinct()

        context = super(ProductView, self).get_context_data(**kwargs)
        context['object_list'] = queryset
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "product/product_detail.html"

    def post(self, request, slug):
        text = request.POST.get("text")
        product = get_object_or_404(Product, slug=slug)
        add_comment = Comment.objects.create(user=request.user, product=product, text=text)
        return JsonResponse({
            "status": "success",
            "comment_id": add_comment.id,
            "comment_text": add_comment.text,
            "user_phone": add_comment.user.phone,
            "user_profile_image": add_comment.user.profile_image.url if add_comment.user.profile_image else '{% static "img/d_profile.png" %}',
            "created_at": add_comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.ratings.filter(product__slug=self.object.slug, user_id=self.request.user.id).exists():
            context["is_rating"] = True
        else:
            context["is_rating"] = False

        if self.request.user.saves.filter(user=self.request.user, product__slug=self.object.slug):
            context["is_save"] = True
        else:
            context["is_save"] = False

        return context


class NavbarPartialView(TemplateView):
    template_name = "includes/header.html"

    def get_context_data(self, **kwargs):
        context = super(NavbarPartialView, self).get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class CategoryView(TemplateView):
    template_name = "category.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ContactUsView(View):
    def get(self, request):
        form = ContactUsForm()
        return render(request, "product/contactus.html", {"form": form})

    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            contactus = form.save(commit=False)
            contactus.user = request.user
            contactus.save()
            return redirect("home:home")
        return render(request, "product/contactus.html", {"form": form})


class RatingView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        try:
            rating = Rating.objects.get(product=product, user_id=request.user.id)
            rating.delete()
            return JsonResponse({"response": "on_rating"})
        except:
            Rating.objects.create(product=product, user_id=request.user.id)
            return JsonResponse({"response": "rating"})


class SearchView(ListView):
    paginate_by = 9
    model = Product
    template_name = "product/products_list.html"

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            return Product.objects.filter(title__icontains=q)
        return Product.objects.all()


class SaveProductView(View):
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        try:
            saved_product = SaveProduct.objects.get(user=request.user, product=product)
            saved_product.delete()
            return redirect("product:product_detail", product.slug)
        except:
            SaveProduct.objects.create(user=request.user, product=product)
            return redirect("product:product_detail", product.slug)


class SavedProductListView(ListView):
    model = SaveProduct
    template_name = "product/product_saves.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = None
        query = SaveProduct.objects.filter(user=user)
        return query


class CategoryDetailView(ListView):
    model = Product
    template_name = "product/products_list.html"

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Product.objects.filter(category__slug=slug)
