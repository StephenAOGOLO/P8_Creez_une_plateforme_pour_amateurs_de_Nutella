from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def handler404(request, exception=None):
    page = "acceuil"
    return render(request, "errors/404.html", {"data": page}, status=404)

def handler500(request, exception=None):
    page = "acceuil"
    return render(request, "errors/500.html", {"data": page}, status=500)

def index(request):
    template = 'Du gras, oui, mais de qualité !!!!!!!!!!!!!!!!!'
    return HttpResponse(template)


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
    list_info = ["info_1", "info_2", "info_3"]
    return render(request, "substitute/results.html", {'data': list_info})


def aliment(request):
    list_info = ["info_1", "info_2", "info_3"]
    return render(request, "substitute/aliment.html", {'data': list_info})


def account(request):
    list_info = ["info_1", "info_2", "info_3"]
    return render(request, "substitute/account.html", {'data': list_info})