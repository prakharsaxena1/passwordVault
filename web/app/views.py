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

# Context handlers
def getContext():
    return context

def setContext(context_new):
    context["userinfo"] = context_new["userinfo"]
    context["passwords"] = context_new["passwords"]
    context["notes"] = context_new["notes"]
    context["contacts"] = context_new["contacts"]

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
            return redirect("/app/passwords")
    elif request.method == "POST" and x == 'register':
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        context["userinfo"] = [username, password, email]
        return redirect("/app/passwords")
    # If login failed or GET request
    return redirect("/account/")

# Home page (app/)
def app_home(request):
    return render(request, "app_home.html")

# Download userfile
def downloadUserfile():
    localContext = getContext()
    print(localContext)
    fObj = helpers.getFernetObj(localContext["userinfo"][0], localContext["userinfo"][1])
    dataList = [fObj.encrypt(("userinfo:&ō&:" + ":&ō&:".join(localContext["userinfo"])).encode()).decode()]
    if localContext["passwords"] != []:
        dataList += [fObj.encrypt(("password:&ō&:" + ":&ō&:".join(i)).encode()).decode() for i in localContext["passwords"]]
    if localContext["notes"] != []:
        dataList += [fObj.encrypt(("note:&ō&:" + ":&ō&:".join(i)).encode()).decode() for i in localContext["notes"]]
    if localContext["contacts"] != []:
        dataList += [fObj.encrypt(("contact:&ō&:" + ":&ō&:".join(i)).encode()).decode() for i in localContext["contacts"]]
    file_data = "\n".join(dataList)
    response = HttpResponse(file_data, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{localContext["userinfo"][0]}"'
    return response

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
            return downloadUserfile()

        elif service == "logout":
            setContext({"userinfo":[],"passwords":[],"notes": [],"contacts": []})
            return redirect("/account/")

    elif checkContext() == False and service in services:
        return redirect("/account/")

    elif checkContext() == True and service not in services:
        return render(request, "404.html")

    return redirect("/account/")

@csrf_protect
def js_requests(request,service):
    if request.method == "POST":
        if service == "getPassword":
            return HttpResponse(helpers.genPassword(request.body.decode()))
        
        elif service == "add_password":
            try:
                passwordInfo = helpers.makePassDataList(request.body.decode())
            except Exception as e:
                return HttpResponse(helpers.httpDump({"success": "false", 
                                                      "msgT": "Error adding password",
                                                      "msgD": "Some of the fields are missing, please fill all the required fields."}))
            localContext = getContext()
            localContext["passwords"].append(passwordInfo)
            setContext(context_new=localContext)
            return HttpResponse(helpers.httpDump({"success": "true", "msg": "password_added", "id": passwordInfo[-1]}))
        
        elif service == "add_note":
            try:
                noteList = helpers.makeNoteDataList(request.body.decode())
            except Exception as e:
                return HttpResponse(helpers.httpDump({"success": "false", "msgT": "Note is empty",
                                                      "msgD":"The title and description for the note is missing, please fill all the required fields."}))
            localContext = getContext()
            localContext["notes"].append(noteList)
            setContext(context_new=localContext)
            return HttpResponse(helpers.httpDump({"success": "true", "msg": "note_added", "id": noteList[-1]}))
        
        elif service == "addContact":
            try:
                contact = helpers.makeContactDataList(request.body.decode())
            except Exception as e:
                return HttpResponse(helpers.httpDump({"success": "false", "msgT": "Invalid data",
                                                      "msgD": "The date entered is not valid, please check before submitting again."}))
            localContext = getContext()
            localContext["contacts"].append(contact)
            setContext(context_new=localContext)
            return HttpResponse(helpers.httpDump({"success": "true", "msg": "contact successfully added",  "id": contact[-1]}))
        
        elif service == "changeEmail":
            try:
                updatedEmail = helpers.emailUpdate(request.body.decode())
            except Exception as e:
                return HttpResponse(helpers.httpDump({"success": "false", "msgT": "Invalid email",
                                                      "msgD": "The provided email is not valid, please check the email before submitting again."}))
            localContext = getContext()
            localContext["userinfo"][2] = updatedEmail 
            setContext(context_new=localContext)
            return HttpResponse(helpers.httpDump({"success": "true", "msg": "Email updated"}))
        
        elif service == "sharePass":
            try:
                x = helpers.sharePass_enc(request.body.decode())
            except Exception as e:
                return HttpResponse(helpers.httpDump({"success": "false", "msgT": "Encryption error", "msgD": "Data provided is incomplete, check method used."}))
            return HttpResponse(helpers.httpDump({"success": "true", "msg": x}))

    elif request.method == "DELETE":
        if service == "deletePassword":
            localContext = getContext()
            try:
                passwordInfo = helpers.removeDataList(request.body.decode(), dataList=localContext["passwords"])
            except Exception as e:
                return HttpResponse(helpers.httpDump({"success": "false", 
                                                      "msgT": "Unable to delete password",
                                                      "msgD": "ID supplied does not match any data in the database."}))
            localContext["passwords"] = passwordInfo
            setContext(context_new=localContext)
            return HttpResponse(helpers.httpDump({"success": "true", "msg": "password deleted"}))
        
        elif service == "deleteContact":
            localContext = getContext()
            try:
                contact = helpers.removeDataList(request.body.decode(), dataList=localContext["contacts"])
            except Exception as e:
                return HttpResponse(helpers.httpDump({"success": "false", 
                                                      "msgT": "Unable to delete password",
                                                      "msgD": "ID supplied does not match any data in the database."}))
            localContext["contacts"] = contact
            setContext(context_new=localContext)
            return HttpResponse(helpers.httpDump({"success": "true", "msg": "contact successfully removed"}))
        
        elif service == "deleteNote":
            localContext = getContext()
            try:
                noteList = helpers.removeDataList(request.body.decode(), dataList=localContext["notes"])
            except Exception as e:
                return HttpResponse(helpers.httpDump({"success": "false", 
                                                      "msgT": "Unable to delete password",
                                                      "msgD": "ID supplied does not match any data in the database."}))
            localContext["notes"] = noteList
            setContext(context_new=localContext)
            return HttpResponse(helpers.httpDump({"success": "true", "msg": "note removed"}))

    # elif request.method == "PUT":
    #     if service == "updatePassword":
    #         pass
    #     if service == "updateContact":
    #         pass
    #     if service == "updateNote":
    #         pass
    return render(request, "404.html")
