from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", Home.as_view(), name='home'),
    path("create_product/", CreateProduct.as_view(), name='create_product'),
    path("create_category/", CreateCategory.as_view(), name='create_category'),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
]
