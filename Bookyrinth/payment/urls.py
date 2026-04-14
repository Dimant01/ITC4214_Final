from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='payment_success'),
    path('cancel/', views.cancel_payment, name='cancel_payment')
]