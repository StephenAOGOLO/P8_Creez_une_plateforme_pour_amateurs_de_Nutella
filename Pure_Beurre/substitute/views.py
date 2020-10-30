from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages

# Create your views here.
from .forms import CreateUserForm

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
    list_info = {"story": "Lorem ipsum dolor sit amet,"
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
    return render(request, "substitute/home.html", {'data': list_info})


def results(request):
    list_info = ["info_1", "info_2", "info_3", "info_4", "info_5", "info_6"]
    return render(request, "substitute/results.html", {'data': list_info})


def aliment(request):
    list_info = ["info_1", "info_2", "info_3"]
    return render(request, "substitute/aliment.html", {'data': list_info})


def account(request):
    context = {}
    context["salutation"] = "AHOY !!"
    context["user"] = "Prénom Utilisateur"
    context["mail"] = "utilisateur@purebeurre.com"
    return render(request, "substitute/account.html", context)


def login(request):
    context = {}
    return render(request, "registration/login.html", context)


def register(request):
    #form = UserCreationForm()
    form = CreateUserForm()
    if request.method == "POST":
        #form = UserCreationForm(request.POST)
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            text = "Bienvenue {} !!! Votre compte a bien été créé !!!".format(user)
            messages.success(request, text)
            return redirect("login")
    context = {"form": form}
    return render(request, "registration/register.html", context)
