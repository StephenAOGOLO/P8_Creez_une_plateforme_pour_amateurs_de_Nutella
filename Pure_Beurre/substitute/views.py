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

#def index(request):
#    template = 'Du gras, oui, mais de qualité !!!!!!!!!!!!!!!!!'
#    return HttpResponse(template)


def index(request):
    return homepage(request)

#def search(request, context):
#    raw_data = request.POST.get("raw_data")
#    #session = Data(raw_data)
#    #store_data(session.big_data)
#    result_engine = DataEngine(raw_data)
#    data = result_engine.big_data
#    print(data)
#    #data = session.big_data
#    context["product"] = raw_data
#    context["results"] = data
#    return render(request, "substitute/results.html", context)

def homepage(request):
    #all_users = User.objects.all()
    #a_user = all_users[0]
    a_user = User.objects.filter(username="test")
    for a in a_user:
        print(a.id)
    #print(a_user)
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
        #context = {}
        #search(request, context)
        raw_data = request.POST.get("raw_data")
        #session = Data(raw_data)
        #store_data(session.big_data)
        #result_engine = DataEngine(raw_data)
        raw_data = secure_text(raw_data)
        if is_entry_empty(raw_data)["status"]:
            context["error_entry"] = is_entry_empty(raw_data)["text"]
            return render(request, "substitute/home.html", context)
        result_engine = DataSearch(raw_data)
        data = result_engine.big_data
        if len(data) == 0:
            context["unknow_product"] = "inconnu au bataillon !!! essayez un autre..."
            return render(request, "substitute/home.html", context)
        #context["product"] = raw_data
        found_aliment = next(reversed(data.items()))[1]
        context["product"] = found_aliment
        context["results"] = data
        return render(request, "substitute/results.html", context)
    return render(request, "substitute/home.html", context)


def save(request, p_id, s_id, u_id):
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
    return render(request, "substitute/save.html", context)




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


def aliment(request, pk):
    session = DataAliment(pk)
    aliment = session.aliment
    context = {"aliment": aliment}
    if request.method == "POST":
        pass
        #store_it = request.POST.get(aliment)
        #for e in store_it:
        #    print(e)


    #print(session.get_substitute())
    return render(request, "substitute/aliment.html", context)


def account(request):
    context = {}
    c = Customer.objects.get(user_id=request.user.id)
    the_historic = get_historic(c)
    context["history"] = the_historic
    context["titre_aliment"] = "ALIMENT"
    context["titre_substitut"] = "SUBSTITUT"
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



#def store_data(data):
#    print("\n"+"*"*10)
#    print("STORE DATA")
#    print("*"*10+"\n")
#    data = data["rcvd"]["essentials"]
#    #print(data)
#    check_aliments = "aliments"
#    check_categories = "categories"
#    for k, v in data.items():
#        #print(k)
#        if k == check_categories:
#        #elif k == check_categories and "id" in v.keys():
#            #print(k)
#            for k_1, v_1 in v.items():
#                id_name = v_1["id"]
#                name = v_1["name"]
#                url = v_1["url"]
#                the_categories = CategoryValue(
#                    id_name=id_name,
#                    name=name,
#                    url=url
#                )
#                #print("\n" + "*" * 10)
#                #print("Lancement sauvegarde category")
#                #print("*" * 10 + "\n")
#                the_categories.store_items()
#            #print("\n**** categories creees ****\n")
#    for k, v in data.items():
#        if k == check_aliments:
#            for k_1, v_1 in v.items():
#                #print(v_1["brand"])
#                brand = v_1["brand"]
#                product_name = v_1["product_name"]
#                categories = v_1["categories"]
#                nutriscore = v_1["nutriscore"]
#                purchase_place = str(v_1["purchase_place"])
#                store = str(v_1["store"])
#                url = v_1["url"]
#                the_aliments = AlimentValue(
#                    brand=brand,
#                    product_name=product_name,
#                    category=categories,
#                    nutriscore=nutriscore,
#                    purchase_place=purchase_place,
#                    store=store,
#                    url=url
#                )
#                #print("\n" + "*" * 10)
#                #print("Lancement sauvegarde aliment")
#                #print("*" * 10 + "\n")
#                the_aliments.store_items()
#        else:
#            print("KO")


