from django.shortcuts import redirect, render, HttpResponse
from app.helpers import httpDump, sharepassDecrypt

def gotoHome(request):
    return redirect("home/")

def home(request):
    return render(request, "home.html")

def sharepass(request):
    if request.method == "GET":
        return render(request, "share-pass.html")
    if request.method == "POST":
        try:
            plain = sharepassDecrypt(request.body.decode())
        except Exception as e:
            return HttpResponse(httpDump({ "success": "false", "data": "Invalid key provided" }))
        return HttpResponse(httpDump({ "success": "true", "data": plain }))

def allRoutesHandler(request, service):
    services = ["contact", "guide", "downloads", "account"] 
    if request.method == "GET":
        if service in services:
            return render(request, f"{service}.html")
        else:
            return render(request, "404.html")

