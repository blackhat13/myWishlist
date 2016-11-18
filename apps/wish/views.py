from django.shortcuts import render, redirect
from .models import Users, Movies
from django.contrib import messages
import datetime

now = datetime.datetime.now()

def index(request):
    return render(request, 'wish/index.html')


def home(request):
    if request.session['name']:
        theUser = Users.UserHandler.filter(username = request.session["name"]).last()
        context = {
            'favs': theUser.movies_set.all(),
            'others': Movies.MovieHandler.exclude(owned_by=theUser)
        }
        return render(request, 'wish/home.html', context)
    else:
        context = {
            'items': Movies.MovieHandler.all()
        }
        return render(request, 'wish/home.html', context)


def registerUser(request):
    name = request.POST.get("name_up")
    username = request.POST.get("username_up")
    email = request.POST.get("email_up")
    password = request.POST.get("pwd_up").encode()
    confirmpassword = request.POST.get("passwordconf_up").encode()
    info = Users.UserHandler.register(name, username, email, password)
    if info[0] is True:
        request.session['name'] = username
        return redirect('/home')

    else:
        if Users.UserHandler.validuser(name):
            messages.error(request, 'Enter Full Name', extra_tags='name')

        if Users.UserHandler.validuser(username):
            messages.error(request, 'Username is not long enough!', extra_tags='username')

        if Users.UserHandler.validemail(email):
            messages.error(request, 'Email is not valid', extra_tags='email')

        if Users.UserHandler.validpassword(password):
            messages.error(request, 'Password must be at least 8 characters!', extra_tags='password')

        if Users.UserHandler.matchpasswords(password, confirmpassword):
            messages.error(request, 'Password doesn\'t match!', extra_tags='passwordconfirm')
        return redirect('/')


def loginUser(request):
    email = request.POST.get("email_in")
    password = request.POST.get('pwd_in').encode()
    Users.UserHandler.login(email, password)
    if Users.UserHandler.login(email, password):
        request.session['name'] = Users.UserHandler.filter(email=email).last().username

        return redirect('/home')
    else:
        if Users.UserHandler.validemail(email):
            messages.error(request, 'The Email format is not valid', extra_tags='email')
        if Users.UserHandler.validpassword(password):
            messages.error(request, 'Password must be at least 8 characters!!', extra_tags='password_in')
        return redirect('/')


def addMovie(request):
    if request.session["name"]:
        user = Users.UserHandler.filter(username=request.session["name"]).last()
        movie_by = request.POST.get("movie_by")
        newMsg = request.POST.get("message_in")
        info = Movies.MovieHandler.addMovie(movie_by, newMsg, user)
        if info[0] is True:
            return redirect('/home')
        else:
            if Movies.MovieHandler.validmovie_by(movie_by):
                messages.error(request, 'At least 3 characters', extra_tags='movie_by')

            if Movies.MovieHandler.validmessage(newMsg):
                messages.error(request, 'Message is not long enough. At least 10 characters', extra_tags='message')
            return redirect('/home')


def singleMovie(request, created_by):
    allmovies = Movies.MovieHandler.filter(created_by=created_by)
    context = {
        'author': created_by,
        'movies': allmovies,
        'count': len(allmovies)
    }
    return render(request, 'wish/single_movie.html', context)


def addremove(request):
    if request.session["name"]:
        user = Users.UserHandler.filter(username=request.session["name"]).last()
        if request.POST and request.POST.get("addMe"):
            movieId = request.POST.get("addMe")
            newFav = Movies.MovieHandler.get(id=movieId)
            newFav.owned_by.add(user)
        elif request.POST and request.POST.get("deleteMe"):
            print ("bababab")
            movieId = request.POST.get("deleteMe")
            newFav = Movies.MovieHandler.get(id=movieId)
            newFav.owned_by.remove(user)
        return redirect('/home')


def logout(request):
    request.session.clear()
    return redirect('/')