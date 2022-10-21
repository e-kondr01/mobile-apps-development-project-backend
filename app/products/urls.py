from django.urls import path

from . import views

urlpatterns = [
    path("barcodes", views.BarcodeListView.as_view()),
    path("products", views.ProductListView.as_view()),
    path("product-movements", views.ProductMovementListView.as_view()),
    path("price-changes", views.PriceChangeListView.as_view()),
    path("price-types", views.PriceTypeListView.as_view()),
    path("characteristics", views.CharacteristicListView.as_view()),
    path("products/<str:pk>/amounts", views.ProductAmountsView.as_view()),
    path("products/<str:pk>/prices", views.ProductPricesView.as_view()),
]
