from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView
from django.views import generic
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from .forms import *
from django.http import HttpResponseRedirect
from carts.models import *
from django.db.models import Q
from shop.debug import log_exceptions
from django.views.generic.edit import UpdateView, FormView
# Create your views here.


class HomePageView(ListView):
    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(active=True, item_status__in=["I", "S"])

    def blogs_list(self):
        blogs = Blog.objects.filter(status="P").order_by('-date_created')[:5]
        return blogs

    def get_home_page_products(self):
        products = Product.objects.filter(active=True, item_status__in=["I", "S"])
        new_released_games = products.order_by("-launch_date")[:12]
        featured_playstation_games = products.filter(category__name__in=['PS 4', 'PS 3'],
                                                     is_featured=True).order_by("-date")[:10]
        featured_xbox_games = products.filter(category__name__in=['Xbox One', 'Xbox 360'],
                                              is_featured=True).order_by("-date")[:10]
        new_arrived_products = products.order_by("-date")[:12]

        return new_released_games, featured_playstation_games, featured_xbox_games, new_arrived_products

    def get_home_page_banner(self):
        qs = PromoCard.objects.filter(active=True).order_by("-date")
        top_coverpage = qs.filter(type="coverpage_top").first()
        center_coverpage = qs.filter(type="coverpage_center").first()
        bottom_coverpage = qs.filter(type="coverpage_bottom").first()
        left_banner = qs.filter(type="banner_left").first()
        right_banner = qs.filter(type="banner_right").first()
        return top_coverpage, center_coverpage, bottom_coverpage, left_banner, right_banner

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        try:
            new_released_games, featured_playstation_games, featured_xbox_games, new_arrived_products = self.get_home_page_products()
            top_coverpage, center_coverpage, bottom_coverpage, left_banner, right_banner = self.get_home_page_banner()
            cart_obj, new_obj = Cart.objects.create_or_get_cart(self.request)
            context['cart'] = cart_obj
            context['articles'] = self.blogs_list()
            context['new_released_games'] = new_released_games
            context['new_arrived_products'] = new_arrived_products
            context['featured_playstation_games'] = featured_playstation_games
            context['featured_xbox_games'] = featured_xbox_games
            context['coverpage_top'] = top_coverpage
            context['center_coverpage'] = center_coverpage
            context['bottom_coverpage'] = bottom_coverpage
            context['banner_left'] = left_banner
            context['banner_right'] = right_banner
            print(cart_obj)
        except IndexError:
            print("Product, Blog, Banner Objects Not Available")
        return context


class ProductListView(ListView):
    paginate_by = 20
    template_name = 'shop/product-list.html'
    context_object_name = "products"

    @log_exceptions("Product List Querysets Function")
    def get_queryset(self):
        sort_by = self.request.GET.get("sort_by")
        try:
            queryset = Product.objects.filter(category__slug=self.kwargs.get("slug"), active=True, item_status__in=["I", "S"])
        except IndexError:
            pass
        if self.request.method == "GET":
            if sort_by == "name":
                return queryset.order_by("name")
            elif sort_by == "price":
                return queryset.order_by("mrp")
            else:
                return queryset.order_by("-date")

    @log_exceptions("Product Side List Filter Function")
    def get_side_list_filter(self):
        products = Product.objects.filter(category__slug=self.kwargs.get("slug"), active=True, item_status__in=["I", "S"])
        publishers = products.filter(publisher__name__isnull=False).values("publisher__name").distinct()
        developers = products.filter(developer__name__isnull=False).values("developer__name").distinct()
        genres = products.filter(genre__genre__isnull=False).values("genre__genre").distinct()
        return publishers, developers, genres

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        try:
            context['category'] = Category.objects.get(slug=self.kwargs.get("slug"))
        except IndexError:
            print("category not available")

        publishers, developers, genres = self.get_side_list_filter()
        context['developers'] = developers
        context['publishers'] = publishers
        context['genres'] = genres
        cart_obj, new_obj = Cart.objects.create_or_get_cart(self.request)
        context["cart"] = cart_obj
        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = 'shop/product-details.html'

    def related_product(self):
        slug = self.request.path
        count = 4
        relatedproducts = []
        products = Product.objects.filter(active=True, item_status__in=["I", "S"])
        product = products.filter(slug=slug.replace("/", "")).first()

        for pub in products.filter(publisher=product.publisher).order_by("-launch_date")[:count]:
            relatedproducts.append(pub)
        for dev in products.filter(developer=product.developer).order_by("-launch_date")[:count]:
            relatedproducts.append(dev)
        for cat in products.filter(category=product.category).order_by("-date")[:count]:
            relatedproducts.append(cat)
        return relatedproducts

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.create_or_get_cart(self.request)
        context["cart"] = cart_obj
        print(cart_obj)
        context["related_products"] = self.related_product()
        return context


class ArticleListView(ListView):
    template_name = 'shop/blog.html'
    model = Blog
    context_object_name = "articles"

    def get_queryset(self):
        articles = Blog.objects.filter(status="P").order_by("-date")
        return articles


class ArticleDetailView(DetailView):
    template_name = 'shop/blog-details.html'
    model = Blog
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        try:
            context['recent_articles'] = Blog.objects.filter(status="P").order_by('-date')[:10]
        except IndexError:
            print("Article Not Available or Minimum 5 Articles required to render")
        return context


class SubscriptionPlanView(ListView):
    template_name = 'shop/plan.html'
    context_object_name = 'plans'

    def get_queryset(self):
        self.request.get_raw_uri()
        return Plan.objects.filter(active=True).order_by('duration')


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


def login_register_page(request):
    user_login_form = UserLoginForm(request.POST or None)
    user_signup_form = SignUpForm(request.POST or None)
    context = {
        "login_form": user_login_form,
        "signup_form": user_signup_form,
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
            return HttpResponseRedirect('')

    if user_signup_form.is_valid():
        email = user_signup_form.cleaned_data.get("email")
        password = user_signup_form.cleaned_data.get("password")
        user = User.objects.filter(email=email)
        if not user:
            user_obj = User.objects.create_user(username=email, email=email, password=password)
            user_obj.save()
            user_login = authenticate(request, username=email, password=password)
            login(request, user_login)
            return redirect("shop:homepage")
        else:
            kwargs = {"error": "User already exist, Please try with different email*"}
            return HttpResponseRedirect('')

    if request.user.is_authenticated:
            return redirect("shop:homepage")
    return render(request, "shop/login-register.html", context)


class ProductSearchView(ListView):
    template_name = "shop/product-list.html"
    context_object_name = "products"

    def get_queryset(self):
        keywords = self.request.GET.get("keywords")
        qs = Product.objects.filter(active=True)
        if keywords:
            return qs.filter(Q(name__icontains=keywords, item_status__in=["S", "I"]))

    def get_context_data(self, **kwargs):
        context = super(ProductSearchView, self).get_context_data(**kwargs)
        qs = self.get_queryset()
        context["developers"] = qs.filter(developer__name__isnull=False).values("developer__name").distinct()
        context["publishers"] = qs.filter(publisher__name__isnull=False).values("publisher__name").distinct()
        context["genres"] = qs.filter(genre__genre__isnull=False).values("genre__genre").distinct()
        return context


class MyOrderView(ListView):
    template_name = "shop/my-orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        user = self.request.user
        carts = Cart.objects.filter(user=user, payment_status="Credit")
        received_orders = []
        for cart in carts:
            orders = cart.orders.order_by("-order_date")
            for order in orders:
                received_orders.append(order)
        return received_orders


class ComingSoonView(TemplateView):
    template_name = "shop/coming-soon.html"


class MyAccountView(FormView):
    template_name = "shop/my-account.html"
    form_class = PersonalDetailForm
    success_url = None

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs["form"] = self.get_form()
            kwargs["user"] = self.request.user
        return super().get_context_data(**kwargs)

class SellYourGamesView(FormView):
    template_name = "shop/sell-your-games.html"
    form_class = SellGamesForm
    success_url = "shop/successful/game-sell-query-submitted-successfuly.html"


