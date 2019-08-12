from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
from .models import *
from django.contrib.auth import authenticate, login
from shop.forms import *
from django.core.cache import cache
from django.http import HttpResponse, Http404
from django.views.decorators.cache import cache_page
from carts.models import *
from django.db.models import Q
from shop.debug import log_exceptions
from django.views.generic.edit import UpdateView, FormView
from shop.emails import send_password_reset_email
from shop.filters import ProductFilter
from django.core.paginator import Paginator
# Create your views here.


def get_cart_obj(request):
    if request.session.get("cart_id"):
        cart_obj = Cart.objects.get(cart_id=request.session.get("cart_id"))
        return cart_obj
    else:
        return ""


class HomePageView(ListView):
    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        cache_key = "_".join([self.request.get_raw_uri(), "homepage_products_lists"])
        cached_value = cache.get(cache_key)
        print(cache_key)
        if cached_value is None:
            products = Product.objects.filter(active=True, item_status__in=["I", "S"])
            cache.set(cache_key, products, 30*60*9)
            return products
        else:
            return cached_value

    def trending_products_list(self):
        cache_key = '_'.join([self.request.get_raw_uri(), "trending_products"])
        cached_value = cache.get(cache_key)
        if cached_value is None:
            atr = Attribute.objects.get(name="trending")
            pd = ProductAttribute.objects.filter(attribute=atr).order_by('-value')[:12]
            products = [at.product for at in pd]
            cache.set(cache_key, products, 30*60*9)
            return products
        else:
            return cached_value

    def get_home_page_products(self):
        new_released_games = cache.get("new_released_games")
        if new_released_games is None:
            new_released_games = self.get_queryset().order_by("-launch_date")[:12]
            cache.set("new_released_games", new_released_games, 30*60*9)

        featured_playstation_games = cache.get("featured_playstation_games")
        if featured_playstation_games is None:
            featured_playstation_games = self.get_queryset().filter(category__name__in=['PS 4', 'PS 3'],
                                                                    is_featured=True).order_by("-date")[:14]
            cache.set("featured_playstation_games", featured_playstation_games, 30*60*9)

        featured_xbox_games = cache.get("featured_xbox_games")
        if featured_xbox_games is None:
            featured_xbox_games = self.get_queryset().filter(category__name__in=['Xbox One', 'Xbox 360'],
                                                             is_featured=True).order_by("-date")[:14]
            cache.set("featured_xbox_games", featured_xbox_games, 30*60*9)
        new_arrived_products = cache.get("new_arrived_products")
        if new_arrived_products is None:
            new_arrived_products = self.get_queryset().order_by("-date")[:12]
            cache.set("new_arrived_products", new_arrived_products, 30*60*9)
        return new_released_games, featured_playstation_games, featured_xbox_games, new_arrived_products


    def get_home_page_banner(self):
        qs = PromoCard.objects.filter(active=True).order_by("-date")
        top_coverpage = qs.filter(promocard_type="coverpage_top")[:3]
        center_coverpage = qs.filter(promocard_type="coverpage_center").first()
        bottom_coverpage = qs.filter(promocard_type="coverpage_bottom").first()
        left_banner = qs.filter(promocard_type="banner_left").first()
        right_banner = qs.filter(promocard_type="banner_right").first()
        return top_coverpage, center_coverpage, bottom_coverpage, left_banner, right_banner

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        try:
            new_released_games, featured_playstation_games, featured_xbox_games, new_arrived_products = self.get_home_page_products()
            top_coverpage, center_coverpage, bottom_coverpage, left_banner, right_banner = self.get_home_page_banner()
            context['cart'] = get_cart_obj(self.request)
            blogs = cache.get("homepage_blogs")
            context['articles'] = blogs
            context['trending_products'] = self.trending_products_list()
            context['new_released_games'] = new_released_games
            context['new_arrived_products'] = new_arrived_products
            context['featured_playstation_games'] = featured_playstation_games
            context['featured_xbox_games'] = featured_xbox_games
            context['coverpage_top'] = top_coverpage
            context['center_coverpage'] = center_coverpage
            context['bottom_coverpage'] = bottom_coverpage
            context['banner_left'] = left_banner
            context['banner_right'] = right_banner
        except IndexError:
            print("Product, Blog, Banner Objects Not Available")
        return context


class ProductListView(ListView):
    template_name = 'shop/products/product_list/product-list.html'
    paginate_by = 20
    
    @log_exceptions("Product List Querysets Function")
    def get_queryset(self):
        cache_key = self.request.get_raw_uri()
        cached_value = cache.get(cache_key)
        rent = self.request.GET.get("rent", None)
        keywords = self.request.GET.get("keywords", None)
        if cached_value is None:
            if keywords:
                queryset = Product.objects.filter(name__icontains=keywords, active=True, item_status__in=["I"])
            else:
                categories = Category.objects.filter(slug=self.kwargs.get("slug")).get_descendants(include_self=True)
                queryset = Product.objects.filter(category__in=categories, active=True, item_status__in=["I"])
            if rent:
                product_attributes = ProductAttribute.objects.filter(attribute__name="game_based_plan_price", value__isnull=False).values_list('product', flat=True).distinct()
                queryset = queryset.filter(id__in=product_attributes)
            cache.set(cache_key, queryset, 9600)
        else:
            queryset = cached_value
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        keywords = self.request.GET.get("keywords", None)
        product_list = ProductFilter(self.request.GET, queryset=self.get_queryset())
        page = self.request.GET.get("page", 1)
        paginator = Paginator(product_list.qs, 20)
        try:
            products = paginator.page(page)
        except PageNotInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        if keywords:
            context["filter_categories"] = None
        else:
            context["filter_categories"] = Category.objects.get(slug=self.kwargs.get("slug"))
        context["products"] = products
        context["products_form"] = product_list.form
        context["paginator"] = paginator
        context["cart"] = get_cart_obj(self.request)
        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = 'shop/products/product_details/product-details.html'

    def get_object(self, queryset=None):
        obj = super(ProductDetailView, self).get_object(queryset=queryset)
        cache_key = self.request.get_raw_uri()
        cached_value = cache.get(cache_key)
        if cached_value is None:
            cache.set(cache_key, obj, 9600)
            cached_value = cache.get(cache_key)
        if not cached_value.active:
            raise Http404()
        return cached_value

    def related_product(self):
        count = 4
        relatedproducts = []
        products = Product.objects.filter(active=True, item_status__in=["I", "S"])
        product = self.get_object()
        cache_key = "related_products_".join(self.request.get_raw_uri())
        cached_value = cache.get(cache_key)
        if cached_value is None:
            for pub in products.filter(publisher=product.publisher).order_by("-launch_date")[:count]:
                relatedproducts.append(pub)
            for dev in products.filter(developer=product.developer).order_by("-launch_date")[:count]:
                relatedproducts.append(dev)
            for cat in products.filter(category=product.category).order_by("-date")[:count]:
                relatedproducts.append(cat)
            cache.set(cache_key, relatedproducts, 9600)
            return relatedproducts
        return cached_value

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context["cart"] = get_cart_obj(self.request)
        context["related_products"] = self.related_product()
        return context


class SubscriptionPlanView(ListView):
    template_name = 'shop/plans/plan.html'
    context_object_name = 'plans'

    def get_queryset(self):
        cache_key = "game_hunter_rental_plan_list"
        cached_value = cache.get(cache_key)
        if cached_value:
            return cached_value
        else:
            plans = Plan.objects.filter(active=True).order_by('duration').exclude(type="GB")
            return plans


class SubscriptionDetailView(DetailView):
    template_name = 'shop/plans/plan-detail.html'
    model = Plan
    context_object_name = 'plan'

    def get_context_data(self, **kwargs):
        context = super(SubscriptionDetailView, self).get_context_data(**kwargs)
        context['cart'] = get_cart_obj(self.request)
        return context


class AboutUsView(TemplateView):
    template_name = 'shop/static/about-us.html'


class ContactUsView(TemplateView):
    template_name = 'shop/static/contact.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'shop/static/privacy-policy.html'


class ReturnCancellationView(TemplateView):
    template_name = 'shop/static/return-cancellation.html'


class ShipplingPolicyView(TemplateView):
    template_name = 'shop/static/shipping-information.html'


class FaqView(TemplateView):
    template_name = 'shop/static/faq.html'


class TermConditionView(TemplateView):
    template_name = 'shop/static/term-condition.html'


def login_register_page(request):
    user_login_form = UserLoginForm(request.POST or None)
    user_signup_form = SignUpForm(request.POST or None)
    context = {
        "login_form": user_login_form,
        "signup_form": user_signup_form,
    }
    if request.session.get("error", None):
        context["error"] = request.session["error"]
        del request.session["error"]
    else:
        pass
    if user_login_form.is_valid():
        username = user_login_form.cleaned_data.get("username")
        password = user_login_form.cleaned_data.get("password")

        if "@" in username:
            try:
                user = User.objects.get(email=username)
                kwargs = {"username": user.username}
            except ObjectDoesNotExist:
                request.session["error"] = "Incorrect username or password"
                return HttpResponseRedirect("")
        else:
            kwargs = {"username": username}
        user = authenticate(request, **kwargs, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            request.session["error"] = "Incorrect username or password"
            return HttpResponseRedirect("")

    if user_signup_form.is_valid():
        email = user_signup_form.cleaned_data.get("email")
        password = user_signup_form.cleaned_data.get("password")
        confirm_password = user_signup_form.cleaned_data.get("confirm_password")
        user = User.objects.filter(email=email)
        if not user:
            if password == confirm_password:
                user_obj = User.objects.create_user(username=email, email=email, password=password)
                user_obj.save()
                user_login = authenticate(request, username=email, password=password)
                login(request, user_login)
                return redirect("shop:homepage")
            else:
                request.session["error"] = "Password not matched"
                return HttpResponseRedirect('')
        else:
            request.session["error"] = "User already exist!"
            return HttpResponseRedirect('')

    if request.user.is_authenticated:
            return redirect("shop:homepage")
    return render(request, "shop/registrations/login-register.html", context)


class MyOrderView(ListView):
    template_name = "shop/my-account/my-orders/my-orders.html"
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
    template_name = "shop/static/coming-soon.html"


class MyAccountView(TemplateView):
    password_reset_form = ResetPasswordForm
    personal_detail_form = PersonalDetailForm
    template_name = "shop/my-account/my-account.html"

    def post(self, request):
        post_data = request.POST or None


class SellYourGamesView(FormView):
    template_name = "shop/sell-your-games.html"
    form_class = SellGamesForm
    success_url = "shop/successful/game-sell-query-submitted-successfuly.html"

    def form_valid(self, form):
        game_name = form.cleaned_data["game_name"]
        customer_name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        mobile = form.cleaned_data
        return super().form_valid(form)


def reset_password(request):
    reset_form = ResetPasswordForm(request.POST or None)
    context = {
        'form': reset_form,
    }
    if reset_form.is_valid():
        email = reset_form.cleaned_data.get("email")
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            ""
        else:
            send_password_reset_email(request, user)
            return redirect("shop:password_reset_done")
    else:
        redirect("shop:password_reset")
    return render(request, "shop/registrations/password_reset.html", context)


def clear_cache(request):
    cache.clear()
    return HttpResponse("Cache cleared for website")

from carts.slacknotification import new_product_order_received

def test_view(request):
    new_product_order_received(ProductOrders.objects.get(id=8))
    print("Fired")
    return HttpResponse("Fired")

