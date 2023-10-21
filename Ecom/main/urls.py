from django.urls import path
from .import views

urlpatterns = [
    path('',views.store, name='store'),
    path('Cart/',views.Cart, name='Cart'),
    path('checkout/',views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('details/<str:pk>/',views.details,name='details'),
]
