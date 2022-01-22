from django.shortcuts import redirect, render

def gotoHome(request):
    return redirect("home/")

def home(request):
    return render(request, "home.html")

def contact_page(request):
    return render(request, "contact.html")

def download_page(request):
    return render(request, "downloads.html")

def guide_page(request):
    return render(request, "guide.html")

def sharepass_page(request):
    return render(request, "share-pass.html")

def account_page(request):
    return render(request, "account.html")
