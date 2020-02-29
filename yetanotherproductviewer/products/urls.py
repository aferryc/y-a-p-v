from django.urls import path
import products.views as ProductView

urlpatterns = [
    path("", ProductView.List.as_view(), name="product-list"),
    path("products/", ProductView.List.as_view(), name="product-list"),
    path("products/add/", ProductView.Add.as_view(), name="product-add"),
    path("products/<int:pk>", ProductView.Detail.as_view(), name="product-detail"),
]
