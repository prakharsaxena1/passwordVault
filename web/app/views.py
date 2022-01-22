from django.http.response import HttpResponse
from django.shortcuts import render, redirect
# csrf
from django.views.decorators.csrf import csrf_protect 
# helpers
from . import helpers


# Create your views here.
global context 
context = {
    "userinfo":[],
    "passwords":[],
    "notes": [],
    "contacts": []
}

def getContext():
    return context

def setContext(context_new):
    context["userinfo"] = context_new["userinfo"]
    context["passwords"] = context_new["passwords"]
    context["notes"] = context_new["notes"]
    context["contacts"] = context_new["contacts"]
    # print("\n::::::::~  CONTEXT UPDATED  ~::::::::\n")
    # print(context)

def checkContext():
    if context["userinfo"] == []:
        return False
    return True

# It handles signin and signup
def app_account_handler(request, x):
    if request.method == "POST" and x == 'login':
        username = request.POST["username"]
        password = request.POST["password"]
        userfile = request.FILES['userfile'].readlines()
        if helpers.login_pass(username, password, userfile[0]):
            fObj = helpers.getFernetObj(username,password)
            for i in userfile:
                temp = fObj.decrypt(i).decode().split(":&ō&:")
                if temp[0] == "userinfo":
                    context["userinfo"] = temp[1::]
                elif temp[0] == "password":
                    context["passwords"].append(temp[1::])
                elif temp[0] == "note":
                    context["notes"].append(temp[1::])
                elif temp[0] == "contact":
                    context["contacts"].append(temp[1::])
            # print(context)
            return redirect("/app/passwords")
    elif request.method == "POST" and x == 'register':
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        context["userinfo"] = [username, password, email]
        return redirect("/app/passwords")
    # If login failed or GET request
    return redirect("/account/")

# Home page
def app_home(request):
    return render(request, "app_home.html")

# Routes handler
def routingFunction(request, service):
    services = ["profile","passwordLab", "passwords", "secure_note", "sharepass", "download_uf", "logout" ]

    if checkContext() == True and service in services:
        if service == "profile":
            context = getContext()
            return render(request, "app_profile.html", {"contacts": context["contacts"], "userinfo": context["userinfo"]})

        elif service == "passwordLab":
            return render(request, "app_passwordLab.html")

        elif service == "passwords":
            context = getContext()
            return render(request, "app_passwords.html", {"passwords": context["passwords"]})

        elif service == "secure_note":
            context = getContext()
            return render(request, "app_secure_notes.html", {"notes": context["notes"]})

        elif service == "sharepass":
            context = getContext()
            return render(request, "app_sharepass.html", {"contacts": context["contacts"]})

        elif service == "download_uf":
            print("convert context to userfile")
            return HttpResponse("app_download_uf")

        elif service == "logout":
            setContext({"userinfo":[],"passwords":[],"notes": [],"contacts": []})
            return redirect("/account/")

    elif checkContext() == False and service in services:
        return redirect("/account/")

    return render(request, "404.html")



@csrf_protect
def js_requests(request,service):
    if request.method == "POST":
        if service == "getPassword":
            return HttpResponse(helpers.genPassword(request.body.decode()))
        
        elif service == "add_password":
            localContext = getContext()
            localContext["passwords"].append(helpers.makePassDataList(request.body.decode()))
            setContext(context_new=localContext)
            return HttpResponse(helpers.httpDump({"msg": "password_added"}))
        
        elif service == "add_note":
            # localContext = getContext()
            # localContext["notes"].append(helpers.makePassDataList(request.body.decode()))
            # setContext(context_new=localContext)
            print(request.body.decode())
            return HttpResponse(helpers.httpDump({"msg": "note_added"}))
        
        elif service == "addContact":
            localContext = getContext()
            localContext["contacts"].append(helpers.makeContactDataList(request.body))
            setContext(context_new=localContext)
            # On success
            return HttpResponse(helpers.httpDump({"success": "true"}))
        
        elif service == "changeEmail":
            try:
                updatedEmail = helpers.emailUpdate(request.body.decode())
            except Exception as e:
                return HttpResponse(helpers.httpDump({"success": "false", "msg": e}))
            localContext = getContext()
            localContext["userinfo"][2] = updatedEmail 
            setContext(context_new=localContext)
            # On success
            return HttpResponse(helpers.httpDump({"success": "true"}))
            
    return render(request, "404.html")