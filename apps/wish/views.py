from django.shortcuts import render, redirect
from .models import Users, Quotes
from django.contrib import messages
import datetime
now = datetime.datetime.now()

def index(request):
    return render(request, 'wish/index.html')


def home(request):
    if request.session['name']:
        userGuy = Users.UserManager.filter(username=request.session["name"]).last()
        context = {
            'favs': userGuy.quotes_set.all(),
            'others': Quotes.QuoteManager.exclude(owned_by=userGuy)
        }
        return render(request, 'wish/home.html', context)
    else:

        context = {
            'items': Quotes.QuoteManager.all()
        }
        return render(request, 'wish/home.html', context)


def registerUser(request):
    name = request.POST.get("name_up")
    username = request.POST.get("username_up")
    email = request.POST.get("email_up")
    password = request.POST.get("pwd_up").encode()
    confirmpassword = request.POST.get("passwordconf_up").encode()
    info = Users.UserManager.register(name, username, email, password)
    if info[0] is True:
        request.session['name'] = username
        return redirect('/home')

    else:
        if Users.UserManager.validuser(name):
            messages.error(request, 'Enter Full Name', extra_tags='name')

        if Users.UserManager.validuser(username):
            messages.error(request, 'Username is not long enough!', extra_tags='username')

        if Users.UserManager.validemail(email):
            messages.error(request, 'Email is not valid', extra_tags='email')

        if Users.UserManager.validpassword(password):
            messages.error(request, 'Password must be at least 8 characters!', extra_tags='password')

        if Users.UserManager.matchpasswords(password, confirmpassword):
            messages.error(request, 'Password Confirmation doesn\'t match!', extra_tags='passwordconfirm')
        return redirect('/')


def loginUser(request):
    email = request.POST.get("email_in")
    password = request.POST.get('pwd_in').encode()
    Users.UserManager.login(email, password)
    if Users.UserManager.login(email, password):
        request.session['name'] = Users.UserManager.filter(email=email).last().username

        return redirect('/home')
    else:
        if Users.UserManager.validemail(email):
            messages.error(request, 'Email format is not valid', extra_tags='email')
        if Users.UserManager.validpassword(password):
            messages.error(request, 'Password must be at least 8 characters!!', extra_tags='password_in')
        return redirect('/')


def addQuote(request):
    if request.session["name"]:
        user = Users.UserManager.filter(username=request.session["name"]).last()
        quoted_by = request.POST.get("quoted_by")
        newMsg = request.POST.get("message_in")
        info = Quotes.QuoteManager.addQuote(quoted_by, newMsg, user)
        if info[0] is True:
            return redirect('/home')
        else:
            if Quotes.QuoteManager.validquoted_by(quoted_by):
                messages.error(request, 'At least 3 characters', extra_tags='quoted_by')

            if Quotes.QuoteManager.validmessage(newMsg):
                messages.error(request, 'Message is not long enough. At least 10 characters', extra_tags='message')
            return redirect('/home')


def singleQuote(request, created_by):
    allquotes = Quotes.QuoteManager.filter(created_by=created_by)
    context = {
        'author': created_by,
        'quotes': allquotes,
        'count': len(allquotes)
    }
    return render(request, 'wish/single_quote.html', context)


def addremove(request):
    if request.session["name"]:
        user = Users.UserManager.filter(username=request.session["name"]).last()
        if request.POST and request.POST.get("addMe"):
            quoteId = request.POST.get("addMe")
            newFav = Quotes.QuoteManager.get(id=quoteId)
            newFav.owned_by.add(user)
        elif request.POST and request.POST.get("deleteMe"):
            print "Nana"
            quoteId = request.POST.get("deleteMe")
            newFav = Quotes.QuoteManager.get(id=quoteId)
            newFav.owned_by.remove(user)
        return redirect('/home')


def logout(request):
    request.session.clear()
    return redirect('/')