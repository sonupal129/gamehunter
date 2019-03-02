from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView
from django.views import generic
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm, SignUpForm
from carts.models import Cart
from django.http import HttpResponseRedirect
from django.db.models import Q
from shop.debug import log_exceptions
# Create your views here.


class HomePageView(ListView):
    template_name = 'shop/index.html'
    context_object_name = 'products'
    model = Product

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        try:
            context['articles'] = Blog.objects.order_by('-date_created')[:5]
            context['new_arrived_products'] = Product.objects.filter(active=True, item_status="I").order_by("-date")[
                                              :12]
            context['featured_playstation_games'] = Product.objects.filter(category__name__in=['PS 4', 'PS 3'],
                                                                           active=True, item_status='I',
                                                                           is_featured=True).order_by('-date')[:10]
            context['featured_xbox_games'] = Product.objects.filter(category__name__in=['Xbox One', 'Xbox 360'],
                                                                    item_status='I', active=True,
                                                                    is_featured=True).order_by('-date')[:10]
            context['coverpage_top'] = PromoCard.objects.filter(active=True, type="coverpage_top").order_by(
                "-date").first()
            context['center_coverpage'] = \
                PromoCard.objects.filter(active=True, type="coverpage_center").order_by("-date").first()
            context['bottom_coverpage'] = \
                PromoCard.objects.filter(active=True, type="coverpage_bottom").order_by("-date").first()
            context['banner_left'] = PromoCard.objects.filter(active=True, type="banner_left").order_by("-date").first()
            context['banner_right'] = PromoCard.objects.filter(active=True, type="banner_right").order_by(
                "-date").first()
        except IndexError:
            print("Product, Blog, Banner Objects Not Available")
        return context

    def get_queryset(self):
        return Product.objects.filter(active=True, item_status="I")


class ProductListView(ListView):
    paginate_by = 20
    template_name = 'shop/product-list.html'
    context_object_name = "products"

    @log_exceptions("Category View")
    def get_queryset(self):
        try:
            queryset = Product.objects.filter(category__slug=self.kwargs.get("slug"), active=True)
        except IndexError:
            print("Category Not Available")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        try:
            context['category'] = Category.objects.get(slug=self.kwargs.get("slug"))
        except IndexError:
            print("category not available")

        context['developers'] = Product.objects.filter(category__slug=self.kwargs.get("slug"), active=True,
                                                       developer__name__isnull=False).values(
            "developer__name").distinct()
        context['publishers'] = Product.objects.filter(category__slug=self.kwargs.get("slug"), active=True,
                                                       publisher__name__isnull=False).values(
            "publisher__name").distinct()
        context['genres'] = Product.objects.filter(category__slug=self.kwargs.get("slug"), active=True,
                                                   genre__genre__isnull=False).values("genre__genre").distinct()
        cart_obj, new_obj = Cart.objects.create_or_get_cart(self.request)
        context["cart"] = cart_obj
        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = 'shop/product-details.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.create_or_get_cart(self.request)
        context["cart"] = cart_obj
        return context


class ArticleListView(ListView):
    template_name = 'shop/blog.html'
    model = Blog
    context_object_name = "articles"


class ArticleDetailView(DetailView):
    template_name = 'shop/blog-details.html'
    model = Blog
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        try:
            context['recent_articles'] = Blog.objects.all().order_by('-date')[:10]
        except IndexError:
            print("Article Not Available or Minimum 5 Articles required to render")
        return context


class SubscriptionPlanView(ListView):
    template_name = 'shop/plan.html'
    context_object_name = 'plans'

    def get_queryset(self):
        return Plan.objects.all().order_by('duration')


class SubscriptionDetailView(DetailView):
    template_name = 'shop/plan-detail.html'
    model = Plan
    context_object_name = 'plan'

    def get_context_data(self, **kwargs):
        context = super(SubscriptionDetailView, self).get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.create_or_get_cart(self.request)
        context['cart'] = cart_obj
        return context


class AboutUsView(TemplateView):
    template_name = 'shop/about-us.html'



def contact_us(request):
     return render(request, 'shop/contact.html')


class PrivacyPolicyView(TemplateView):
    template_name = 'shop/privacy-policy.html'


class ReturnCancellationView(TemplateView):
    template_name = 'shop/return-cancellation.html'


class ShipplingPolicyView(TemplateView):
    template_name = 'shop/shipping-information.html'


class FaqView(TemplateView):
    template_name = 'shop/faq.html'


class TermConditionView(TemplateView):
    template_name = 'shop/term-condition.html'


def login_page(request):
    user_login_form = UserLoginForm(request.POST or None)

    context = {
        "form": user_login_form,
    }
    if user_login_form.is_valid():
        username = user_login_form.cleaned_data.get("username")
        password = user_login_form.cleaned_data.get("password")

        if "@" in username:
            user = User.objects.get(email=username)
            kwargs = {"username": user.username}
        else:
            kwargs = {"username": username}
        user = authenticate(request, **kwargs, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            context["error"] = "Incorrect username or password*"
            redirect("shop:login")
    if request.user.is_authenticated:
        return redirect("shop:homepage")
    return render(request, "shop/login.html", context)


def signup_page(request):
    signup_form = SignUpForm(request.POST or None)
    context = {
        "form": signup_form,
    }
    if signup_form.is_valid():
        email = signup_form.cleaned_data.get("email")
        password = signup_form.cleaned_data.get("password")
        user = User.objects.filter(email=email)
        if not user:
            user_obj = User.objects.create_user(username=email, email=email, password=password)
            user_obj.save()
            user_login = authenticate(request, username=email, password=password)
            login(request, user_login)
            return redirect("shop:homepage")
        else:
            context["error"] = "User already exist, Please try with different email*"
            redirect("shop:signup")
    if request.user.is_authenticated:
        return redirect("shop:homepage")
    return render(request, 'shop/register.html', context)


def product_search(request):
    keywords = request.GET.get("keywords")

    if keywords == "":
        return render(request, "shop/no-search-product-list-found.html")
    elif keywords is not None:
        context = {
            'developers': Product.objects.filter(name__icontains=keywords, active=True,
                                                 developer__name__isnull=False).values(
                "developer__name").distinct(),
            'publishers': Product.objects.filter(name__icontains=keywords, active=True,
                                                 publisher__name__isnull=False).values(
                "publisher__name").distinct(),
            'genres': Product.objects.filter(name__icontains=keywords, active=True,
                                             genre__genre__isnull=False).values("genre__genre").distinct(),
            'categories': Product.objects.filter(name__icontains=keywords, active=True,
                                                 category__name__isnull=False).values(
                "category__name").distinct(),
            'products': Product.objects.filter(Q(name__icontains=keywords) | Q(description__icontains=keywords))
        }
        return render(request, "shop/search-product-list.html", context)
    return render(request, "shop/no-search-product-list-found.html")

