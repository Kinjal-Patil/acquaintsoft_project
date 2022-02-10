from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import *

from .forms import SignupForm, ProductForm, CategoryForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

from .models import Products, Category


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        print(form, "\n\n\n")
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return render(request=request, template_name="signin.html", context={"signup_form": form})
        messages.error(request, "Unsuccessful registration. Invalid information.")
        return redirect('signup')
        # return render(request=request, template_name="signup.html", context={"signup_form": form})
    form = SignupForm()
    return render(request=request, template_name="signup.html", context={"signup_form": form})


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="signin.html", context={"login_form": form})


class Home(ListView):
    model = User
    template_name = "home.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('signup')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['product_list'] = Products.objects.filter(is_del=False)
        kwargs['category'] = Products.objects.filter(is_del=False)
        return kwargs


class CreateProduct(CreateView):
    model = Products
    form_class = ProductForm
    template_name = "create_product.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('signup')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.add_by = self.request.user
        self.object.user_id = self.request.user
        self.object.save()
        messages.success(self.request, "Product is created successfully")
        return redirect('create_product')


class ProductList(ListView):
    model = Products
    template_name = "home.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('signup')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['product_list'] = Products.objects.filter(is_del=False)
        return kwargs


class ProductUpdateView(UpdateView):
    model = Products
    form_class = ProductForm
    template_name = 'edit_products.html'
    pk_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('signup')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.modify_by = self.request.user
        post.modify_date = timezone.now()
        post.save()
        return redirect('home')


class CreateCategory(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "create_category.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('signup')
        if not request.user.is_superuser:
            messages.error(request, "You are not allowed to add Category")
            return HttpResponseRedirect('signup')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.add_by = self.request.user
        self.object.save()
        messages.success(self.request, "Category is created successfully")
        return redirect("create_category")


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ('name',)
    template_name = 'edit_category.html'
    pk_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('signup')
        if not request.user.is_superuser:
            messages.error(request, "You are not allowed to add Category")
            return HttpResponseRedirect('signup')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.modify_by = self.request.user
        post.modify_date = timezone.now()
        post.save()
        return redirect('home')
