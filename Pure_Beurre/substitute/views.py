from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login as lgi, logout as lgo
from django.contrib import messages

# Create your views here.
from .forms import CreateUserForm

from .operations import Data

from .Values import AlimentValue, CategoryValue

from .models import *

def handler404(request, exception=None):
    page = "acceuil"
    return render(request, "errors/404.html", {"data": page}, status=404)

def handler500(request, exception=None):
    page = "acceuil"
    return render(request, "errors/500.html", {"data": page}, status=500)

#def index(request):
#    template = 'Du gras, oui, mais de qualité !!!!!!!!!!!!!!!!!'
#    return HttpResponse(template)


def index(request):
    return homepage(request)


def homepage(request):
    context = {"story": "Lorem ipsum dolor sit amet,"
                          " consectetur adipiscing elit."
                          " Sed non risus."
                          " Suspendisse lectus tortor,"
                          " dignissim sit amet,"
                          " adipiscing nec, ultricies sed, dolor."
                          " Cras elementum ultrices diam."
                          " Maecenas ligula massa, varius a,"
                          " semper congue, euismod non, mi."
                          " Proin porttitor, orci nec nonummy molestie,"
                          " enim est eleifend mi, non fermentum diam nisl sit amet erat."
                          " Duis semper. Duis arcu massa, scelerisque vitae,"
                          " consequat in, pretium a, enim."
                          " Pellentesque congue."
                          " Ut in risus volutpat libero pharetra tempor.",
            "sentence": "Lorem ipsum dolor sit amet,"
                        " consectetur adipiscing elit."
                        " Sed non risus. Suspendisse lectus tortor,"
                        " dignissim sit amet,"
                        " adipiscing nec, ultricies sed, dolor."
                        " Cras elementum ultrices diam.",
                 "goal": "Trouvez un produit de substitution pour ceux que vous consommez tous les jours"}
    if request.method == "POST":
        raw_data = request.POST.get("raw_data")
        session = Data(raw_data)
        store_data(session.big_data)
        data = session.big_data
        context["product"] = raw_data
        context["results"] = data
        return render(request, "substitute/results.html", context)
    return render(request, "substitute/home.html", context)


#def store_aliment(data):
#    an_aliment = Aliment(
#        brand=data.brand,
#        name=data.product_name,
#        category=data.categories,
#        nutriscore=data.nutriscore,
#        purchase_places=data.purchase_place,
#        store=data.store,
#        url=data.url
#    )
#    an_aliment.save()
#
#
#def store_category(data):
#    a_category = Category(
#        id=data.id,
#        name=data.name,
#        url=data.url
#    )
#    a_category.save()
#
#
#def store_data(data):
#    data = data["rcvd"]["essentials"]
#    print(data)
#    for k, v in data.items():
#        brand = v["brand"]
#        product_name = v["product_name"]
#        nutriscore = v["nutriscore"]
#        purchase_place = str(v["purchase_place"])
#        store = str(v["store"])
#        url = v["url"]
#    store_aliment(data)
#    store_category()

def results(request):
    list_info = ["info_1", "info_2", "info_3", "info_4", "info_5", "info_6"]
    return render(request, "substitute/results.html", {'data': list_info})


def aliment(request):
    context = {}
    raw_data = "biscuit"
    session = Data(raw_data)
    data = session.big_data
    context["product"] = raw_data
    context["results"] = data
    context["opfofa"] = "https://fr.openfoodfacts.org"
    return render(request, "substitute/aliment.html", context)


def account(request):
    context = {}
    context["salutation"] = "AHOY !!"
    context["mail"] = "utilisateur@purebeurre.com"
    return render(request, "substitute/account.html", context)


def login(request):
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
    if request.user.is_authenticated:
        return redirect("/substitute/account")
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get("username")
                text = "Bienvenue {} !!! Votre compte a bien été créé !!!".format(user)
                messages.success(request, text)
                return redirect("login")
        context = {"form": form}
        return render(request, "registration/register.html", context)


def is_user_authenticate(request):
    if request.user.is_authenticated:
        return redirect("/substitute/account")



def store_data(data):
    print("\n"+"*"*10)
    print("STORE DATA")
    print("*"*10+"\n")
    data = data["rcvd"]["essentials"]
    #print(data)
    check_aliments = "aliments"
    check_categories = "categories"
    for k, v in data.items():
        #print(k)
        if k == check_categories:
        #elif k == check_categories and "id" in v.keys():
            print(k)
            for k_1, v_1 in v.items():
                id_name = v_1["id"]
                name = v_1["name"]
                url = v_1["url"]
                the_categories = CategoryValue(
                    id_name=id_name,
                    name=name,
                    url=url
                )
                print("\n" + "*" * 10)
                print("Lancement sauvegarde category")
                print("*" * 10 + "\n")
                the_categories.store_items()
        if k == check_aliments:
            for k_1, v_1 in v.items():
                #print(v_1["brand"])
                brand = v_1["brand"]
                product_name = v_1["product_name"]
                categories = v_1["categories"]
                nutriscore = v_1["nutriscore"]
                purchase_place = str(v_1["purchase_place"])
                store = str(v_1["store"])
                url = v_1["url"]
                the_aliments = AlimentValue(
                    brand=brand,
                    product_name=product_name,
                    category=categories,
                    nutriscore=nutriscore,
                    purchase_place=purchase_place,
                    store=store,
                    url=url
                )
                #print("\n" + "*" * 10)
                #print("Lancement sauvegarde aliment")
                #print("*" * 10 + "\n")
                the_aliments.store_items()
        else:
            print("KO")