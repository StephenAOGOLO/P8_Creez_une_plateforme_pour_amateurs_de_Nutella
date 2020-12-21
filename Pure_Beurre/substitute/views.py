from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as usr

from django.contrib.auth import authenticate, login as lgi, logout as lgo
from django.contrib import messages

# Create your views here.
from .forms import CreateUserForm

#from .operations import Data, DataEngine, DataSearch, DataAliment
from .operations import *

#from .Values import AlimentValue, CategoryValue

from .models import *


def handler404(request, exception=None):
    page = "acceuil"
    return render(request, "errors/404.html", {"data": page}, status=404)


def handler500(request, exception=None):
    page = "acceuil"
    return render(request, "errors/500.html", {"data": page}, status=500)


def index(request):
    return homepage(request)


def search(request, product):
    if "browser_product" in request.POST:
        browser_product = request.POST.get("browser_product")
        print(browser_product)
        return redirect("/substitute/search/product={}".format(browser_product))
    text = get_text()
    context = {"text": text,
               "goal": "Trouvez un produit de substitution pour ceux que vous consommez tous les jours"}
    raw_data = secure_text(product)
    result_engine = DataSearch(raw_data)
    data = result_engine.big_data
    if len(data) == 0:
        msg = "Produit inconnu au bataillon !!! Veuillez reformuler votre saisie ou essayez un autre..."
        print("search len(data) : {}".format(request))
        messages.error(request, msg)
        return redirect("/substitute/home")
    found_aliment = next(reversed(data.items()))[1]
    context["product"] = found_aliment
    context["product_nutriscore"] = set_nutriscore_tag(found_aliment.nutriscore)
    context["results"] = data
    return render(request, "substitute/search.html", context)






def homepage(request):
    text = get_text()
    context = {"text": text,
               "goal": "Trouvez un produit de substitution pour ceux que vous consommez tous les jours"}
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
    if "browser_product" in request.POST:
        browser_product = request.POST.get("browser_product")
        print(browser_product)
        return redirect("/substitute/search/product={}".format(browser_product))
    context = {}
    p = Aliment.objects.get(id=p_id)
    s = Aliment.objects.get(id=s_id)
    u = User.objects.get(id=u_id)
    c = Customer.objects.get(user_id=u_id)
    record = DataSave(p, s, c)
    record.store_data()
    context["title"] = ["Aliment initial", "Aliment de substitution"]
    context["p"] = p
    context["s"] = s
    context["u"] = u
    context["p_nutriscore"] = set_nutriscore_tag(p.nutriscore)
    context["s_nutriscore"] = set_nutriscore_tag(s.nutriscore)
    return render(request, "substitute/save.html", context)


def aliment(request, p_id, s_id, u_id):
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
    if "browser_product" in request.POST:
        browser_product = request.POST.get("browser_product")
        print(browser_product)
        return redirect("/substitute/search/product={}".format(browser_product))
    context = {}
    c = Customer.objects.get(user_id=request.user.id)
    the_historic = get_historic(c)
    context["salutation"] = "SALUT"
    return render(request, "substitute/account.html", context)


def historic(request):
    if "browser_product" in request.POST:
        browser_product = request.POST.get("browser_product")
        print(browser_product)
        return redirect("/substitute/search/product={}".format(browser_product))
    context = {}
    c = Customer.objects.get(user_id=request.user.id)
    the_historic = get_historic(c)
    if len(the_historic) == 0:
        context["empty"] = "Votre historique est vide"
    context["history"] = the_historic
    context["titre_aliment"] = "ALIMENT"
    context["titre_substitut"] = "SUBSTITUT"
    context["salutation"] = "BIENVENUE"
    context["mail"] = "utilisateur@purebeurre.com"
    return render(request, "substitute/historic.html", context)

def login(request):
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
    lgo(request)
    return redirect("/substitute/home")


def register(request):
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
    if request.user.is_authenticated:
        return redirect("/substitute/account")

def mentions(request):
    text = get_text()
    context = {"text": text}
    return render(request, "substitute/mentions.html", context)