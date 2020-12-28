""" This module handles all the views of the application. """
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as lgi, logout as lgo
from django.contrib import messages

# Create your views here.
from .forms import CreateUserForm
from .operations import *
from .models import *


def handler404(request, exception=None):
    """ This function takes care of 404 errors.
     When a 404 error occurs, the '404.html' is displayed."""
    page = "acceuil"
    return render(request, "errors/404.html", {"data": page}, status=404)


def handler500(request, exception=None):
    """ This function takes care of 500 errors.
     When a 404 error occurs, the '500.html' is displayed."""
    page = "acceuil"
    return render(request, "errors/500.html", {"data": page}, status=500)


def index(request):
    """ This function is a shortcut-like view to the homepge view. """
    return homepage(request)


def search(request, product):
    """ This function is the twin view of homepage().
    It's called to handle the seek of products.
    It is composed of a error handler to secure the user entries."""
    if "browser_product" in request.POST:
        browser_product = request.POST.get("browser_product")
        print(browser_product)
        return redirect("/substitute/search/product={}"
                        .format(browser_product))
    text = get_text()
    context = {"text": text,
               "goal": "Trouvez un produit de substitution"
                       " pour ceux que vous consommez tous les jours"}
    raw_data = secure_text(product)
    result_engine = DataSearch(raw_data)
    data = result_engine.big_data
    if len(data) == 0:
        msg = "Produit inconnu au bataillon !!!" \
              " Veuillez reformuler votre saisie ou essayez un autre..."
        print("search len(data) : {}".format(request))
        messages.error(request, msg)
        return redirect("/substitute/home")
    found_aliment = next(reversed(data.items()))[1]
    context["product"] = found_aliment
    context["product_nutriscore"] = set_nutriscore_tag(found_aliment.nutriscore)
    context["results"] = data
    return render(request, "substitute/search.html", context)


def homepage(request):
    """ This function is the main view of the application. It's rendering the homepage 'home.html',
      where the user can search products or just read contents."""
    text = get_text()
    context = {"text": text,
               "goal": "Trouvez un produit de substitution"
                       " pour ceux que vous consommez tous les jours"}
    if request.method == "POST":
        if "browser_product" in request.POST:
            browser_product = request.POST.get("browser_product")
            print(browser_product)
            return redirect("/substitute/search/product={}".format(browser_product))
        if "product" in request.POST:
            product = request.POST.get("product")
            if is_entry_empty(product)["status"]:
                context["error_entry"] = is_entry_empty(product)["text"]
                print("search is_entry : {}".format(request))
                msg = context["error_entry"]
                messages.error(request, msg)
                return render(request, "substitute/home.html", context)
            return redirect("/substitute/search/product={}".format(product))
    return render(request, "substitute/home.html", context)


def save(request, p_id, s_id, u_id):
    """ This function is called to catch product,
     substitute and user id's before launch a record of swap. """
    if "browser_product" in request.POST:
        browser_product = request.POST.get("browser_product")
        print(browser_product)
        return redirect("/substitute/search/product={}".format(browser_product))
    context = {}
    product = Aliment.objects.get(id=p_id)
    substitute = Aliment.objects.get(id=s_id)
    user = User.objects.get(id=u_id)
    customer = Customer.objects.get(user_id=u_id)
    record = DataSave(product, substitute, customer)
    record.store_data()
    context["title"] = ["Aliment initial", "Aliment de substitution"]
    context["p"] = product
    context["s"] = substitute
    context["u"] = user
    context["p_nutriscore"] = set_nutriscore_tag(product.nutriscore)
    context["s_nutriscore"] = set_nutriscore_tag(substitute.nutriscore)
    return render(request, "substitute/save.html", context)


def aliment(request, p_id, s_id, u_id):
    """ This function is called to get more details on a product. """
    if "browser_product" in request.POST:
        browser_product = request.POST.get("browser_product")
        print(browser_product)
        return redirect("/substitute/search/product={}".format(browser_product))
    s_session = DataAliment(s_id)
    substitute = s_session.aliment
    p_session = DataAliment(p_id)
    product = p_session.aliment
    substitute_nutrscore = set_nutriscore_tag(substitute.nutriscore)
    context = {"substitut": substitute,
               "substitut_nutriscore": substitute_nutrscore,
               "produit": product,
               "utilisateur_id": u_id
               }
    return render(request, "substitute/aliment.html", context)


def account(request):
    """ This function handles account user. """
    if "browser_product" in request.POST:
        browser_product = request.POST.get("browser_product")
        print(browser_product)
        return redirect("/substitute/search/product={}".format(browser_product))
    context = {}
    customer = Customer.objects.get(user_id=request.user.id)
    get_historic(customer)
    context["salutation"] = "SALUT"
    return render(request, "substitute/account.html", context)


def historic(request):
    """ This function handles historic user. """
    if "browser_product" in request.POST:
        browser_product = request.POST.get("browser_product")
        print(browser_product)
        return redirect("/substitute/search/product={}".format(browser_product))
    context = {}
    customer = Customer.objects.get(user_id=request.user.id)
    the_historic = get_historic(customer)
    if len(the_historic) == 0:
        context["empty"] = "Votre historique est vide"
    context["history"] = the_historic
    context["titre_aliment"] = "ALIMENT"
    context["titre_substitut"] = "SUBSTITUT"
    context["salutation"] = "BIENVENUE"
    context["mail"] = "utilisateur@purebeurre.com"
    return render(request, "substitute/historic.html", context)


def login(request):
    """ This function drives the user
     to the login page or the account page,
      depending on authentication status. """
    if "browser_product" in request.POST:
        browser_product = request.POST.get("browser_product")
        print(browser_product)
        return redirect("/substitute/search/product={}".format(browser_product))
    if request.user.is_authenticated:
        return redirect("/substitute/account")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                lgi(request, user)
                return redirect("/substitute/account")
            else:
                messages.info(request, "Les informations saisies sont incorrectes !")
        context = {}
        return render(request, "registration/login.html", context)


def logout(request):
    """ This function redirects
     user to homepage() after log out. """
    lgo(request)
    return redirect("/substitute/home")


def register(request):
    """ This function drives the user
     to the register page or the account page,
    depending on authentication status. """
    if "browser_product" in request.POST:
        browser_product = request.POST.get("browser_product")
        print(browser_product)
        return redirect("/substitute/search/product={}".format(browser_product))
    if request.user.is_authenticated:
        return redirect("/substitute/account")
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get("username")
                a_user = User.objects.get(username=user)
                a_customer = Customer(user_id=a_user.id)
                a_customer.save()
                text = "Bienvenue {} !!! Votre compte a bien été créé !!!".format(user)
                messages.success(request, text)
                return redirect("login")
        context = {"form": form}
        return render(request, "registration/register.html", context)


def is_user_authenticate(request):
    """ This function redirects user if authenticated. """
    if request.user.is_authenticated:
        return redirect("/substitute/account")


def mentions(request):
    """ This function rendering mentions.html with the text stored in the website database.  """
    text = get_text()
    context = {"text": text}
    return render(request, "substitute/mentions.html", context)
