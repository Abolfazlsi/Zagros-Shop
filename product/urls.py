from django.urls import path
from product import views

app_name = "product"
urlpatterns = [
    path("products-list", views.ProductView.as_view(), name="product_list"),
    path("product-detail/<slug:slug>", views.ProductDetailView.as_view(), name="product_detail"),
    path("navbar", views.NavbarPartialView.as_view(), name="navbar"),
    path("category", views.CategoryView.as_view(), name="category"),
    path("contactus", views.ContactUsView.as_view(), name="contactus"),
    path("rating/<slug:slug>", views.RatingView.as_view(), name="rating"),
    path("serach", views.SearchView.as_view(), name="search_product"),
    path("save/<slug:slug>", views.SaveProductView.as_view(), name="save_product"),
    path("saved-products", views.SavedProductListView.as_view(), name="saved_products"),
    path("category-detail/<slug:slug>", views.CategoryDetailView.as_view(), name="category_detail"),
]
