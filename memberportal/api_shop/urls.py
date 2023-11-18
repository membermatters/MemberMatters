from django.urls import path
from . import views

urlpatterns = [
    path(
        "api/shop/products",
        views.AllProducts.as_view(),
        name="shop_product_list",
    ),
]
