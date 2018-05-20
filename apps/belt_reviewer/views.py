from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
import bcrypt

# Create your views here.
def index(request):
    if "user_id" not in request.session:
        return render(request, 'belt_reviewer/index.html')
    return redirect(reverse("home"))


def books(request):
    recent = Review.objects.order_by('-id')[:3]
    data = {
        "user": User.objects.get(id=request.session["user_id"]),
        "recent": reversed(recent),
        "books": Book.objects.all()
    }
    return render(request, 'belt_reviewer/home.html', data)


def add(request):
    return render(request, 'belt_reviewer/add.html')


def new_book(request):
    if request.POST.get('author'):
        author_name = request.POST.get('author')
    else:
        author_name = request.POST.get('authors')
    if not Author.objects.filter(name=author_name):
        author = Author.objects.create(name=author_name)
        author.save()
    else:
        author = Author.objects.get(name=author_name)
    new = Book.objects.create(title=request.POST.get('title'))
    new.save()
    new.authors.add(author)
    review = Review.objects.create(rating=request.POST.get(
        'rating'), content=request.POST.get('content'), user=User.objects.get(id=request.session["user_id"]), book=new)
    review.save()
    return redirect(reverse('show_book', args=[new.id]))


def show_book(request, id):
    book = Book.objects.get(id=id)
    reviews = book.reviews.all()
    return render(request, 'belt_reviewer/book.html', {"book": Book.objects.get(id=id), "reviews": reviews})

def new_review(request, id):
    review = Review.objects.create(rating=request.POST.get(
        'rating'), content=request.POST.get('content'), user=User.objects.get(id=request.session["user_id"]), book=Book.objects.get(id=id))
    review.save()
    return redirect(reverse("show_book", args=[review.book.id]))

def new_user(request):
    valid = User.objects.validations(request.POST)
    if not valid[0]:
        request.session["errors"] = valid[1]
        return redirect(reverse("index"))
    new = User.objects.create(name=request.POST.get('name'), alias=request.POST.get(
        'alias'), email=request.POST.get('reg_email'), password=request.POST.get('reg_password'))
    new.save()
    request.session["user_id"] = new.id
    return redirect(reverse('home'))


def show_user(request, id):
    user = User.objects.get(id=id)
    reviews = user.reviews.all()
    reviews_count = reviews.count()
    return render(request, 'belt_reviewer/user.html', {"user": user,"reviews": reviews, "reviews_count": reviews_count})


def login(request):
    request.session.clear()
    user = User.objects.get(email=request.POST.get("log_email"))
    request.session["user_id"] = user.id
    return redirect(reverse('home'))


def logout(request):
    request.session.clear()
    return redirect(reverse("index"))


def delete_review(request, id):
    review = Review.objects.get(id=id)
    review.delete()
    return redirect(reverse('home'))
