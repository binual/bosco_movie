from dis import show_code
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def adminbosco_dash(request):
    return render(request, 'adminbosco.html')

def admin(request):
    return render(request, 'adminlogin.html')



def admin_bosco_login(request):
    user = None  # Initialize user outside the if block

    if request.method == "POST":
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['uid'] = username
            if user.is_superuser:
                return redirect('adminbosco_dash')
            else:
                return redirect('welcome')
        else:
            messages.error(request, "There is an error in logging in, please try again")

    return render(request, 'adminlogin.html', {'user': user})




def welcome(request):
    return render(request, 'welcome.html')

def add_theater(request):
    if request.method == 'POST':
        theater_name = request.POST.get('theater_name')
        theater_image = request.FILES.get('theater_image')
        owner_name = request.POST.get('owner_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        location = request.POST.get('location')
        address = request.POST.get('address')
        manager_name = request.POST.get('manager_name')
        user=User.objects.create_user(username=username,password=password)
        if  theater_image:
            theater = Theater.objects.create(
                theater_name=theater_name,
                theater_image=theater_image,
                owner_name=owner_name,
                user=user,
                phone_number=phone_number,
                location=location,
                address=address,
                manager_name=manager_name,
                approved=0
            )
           
            return redirect('theater_list')  # Redirect to the theater list or another appropriate URL

    return render(request, 'add_theater.html')  # Change the template name accordingly


def theater_list(request):
    theaters = Theater.objects.all()
    return render(request, 'theater_list.html', {'ct': theaters})


def ownerregister(request):
    if request.method == 'POST':
        theater_name = request.POST.get('theater_name')
        theater_image = request.FILES.get('theater_image')
        owner_name = request.POST.get('owner_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        location = request.POST.get('location')
        address = request.POST.get('address')
        manager_name = request.POST.get('manager_name')
        user=User.objects.create_user(username=username,password=password)
        if theater_image:
            theater = Theater.objects.create(
                theater_name=theater_name,
                theater_image=theater_image,
                owner_name=owner_name,
                user=user,
                phone_number=phone_number,
                location=location,
                address=address,
                manager_name=manager_name,
                approved=1
            )
            
            return redirect('admin_bosco_login') 
        
    return render(request, 'register.html')


def approve(request):
    app=Theater.objects.filter(approved=1)
    return render(request, 'approve.html',{'app':app})

def adminapproval(request,pk):
    adm=Theater.objects.get(id=pk)
    adm.approved=0
    adm.save()
    return redirect('approve')
     


def adminreject(request, pk):
    theater = get_object_or_404(Theater, id=pk)
    theater.delete()
    return redirect('approve')


def edit_theater(request, theater_id):
    theater = Theater.objects.get(id=theater_id)

    if request.method == 'POST':
        theater.theater_name = request.POST.get('theater_name')
        theater.owner_name = request.POST.get('owner_name')
        theater.username = request.POST.get('username')
        theater.password = request.POST.get('password')
        theater.phone_number = request.POST.get('phone_number')
        theater.location = request.POST.get('location')
        theater.address = request.POST.get('address')
        theater.manager_name = request.POST.get('manager_name')
        theater.approved = request.POST.get('approved', 1)  # Default value is 1

        if 'theater_image' in request.FILES:
            theater.theater_image = request.FILES['theater_image']

        # Validate that required fields are not empty
        if (
            theater.theater_name and
            theater.owner_name and
            theater.username and
            theater.password and
            theater.phone_number and
            theater.location and
            theater.address and
            theater.manager_name
        ):
            theater.save()
            return redirect('theater_list')  # Redirect to the theater list or another appropriate URL

    return render(request, 'edit_theater.html', {'theater': theater})



def delete_theater(request, theater_id):
    theater = Theater.objects.get(id=theater_id)
    theater.delete()
    return redirect('theater_list')



def add_movie(request):
    try:
        user_theater = Theater.objects.get(user=request.user)
    except Theater.DoesNotExist:
        return redirect('error_page')

    if request.method == 'POST':
        title = request.POST.get('movie_name')
        genre = request.POST.get('movie_genre')
        release_date = request.POST.get('movie_rdate')
        description = request.POST.get('movie_des')
        rating = request.POST.get('movie_rating')
        duration = request.POST.get('movie_duration')

        # Additional fields such as movie trailer and poster
        movie_trailer = request.FILES.get('movie_trailer')
        movie_poster = request.FILES.get('movie_poster')

        # Create and save the new movie instance
        movie = Movie(
            theater_name=user_theater,
            movie_name=title,
            movie_genre=genre,
            movie_rdate=release_date,
            movie_des=description,
            movie_rating=rating,
            movie_duration=duration,
            movie_trailer=movie_trailer,
            movie_poster=movie_poster
        )
        movie.save()

        return redirect('view_movies')

    return render(request, 'movieregister.html', {'user_theater': user_theater})



def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return redirect('welcome')


def view_movies(request):
    movies = Movie.objects.all()  # You might want to add more specific filters
    return render(request, 'viewmovie.html', {'ct': movies})

def add_show(request):
    try:
        user_theater = Theater.objects.get(user=request.user)
    except Theater.DoesNotExist:
        return redirect('error_page')  # Redirect to an error page if the theater does not exist

    if request.method == 'POST':
        theater_id = request.POST.get('theater_id')
        theater = get_object_or_404(Theater, id=theater_id, user=request.user)
        movie_name = request.POST.get('movie_name')
        times = request.POST.getlist('times')  # Use getlist to get multiple values
        date = request.POST.get('date')
        price = request.POST.get('price')
        movie = get_object_or_404(Movie, id=movie_name)

        # Convert times list to a comma-separated string
        times_str = ', '.join(times)

        # Create a Shows instance with the string representation of times
        Shows.objects.create(
            theater_name=theater,
            movie=movie,
            time=times_str,
            date=date,
            price=price
        )

        return redirect('welcome')  # Redirect to a view where you list all shows

    theaters = Theater.objects.get(user=request.user)
    movies = Movie.objects.all()

    return render(request, 'showregister.html', {'theaters': theaters, 'movies': movies, 'user_theater': user_theater})




def show_list(request):
    shows = Shows.objects.all()  # You might want to add more specific filters
    return render(request, 'viewshow.html', {'ct': shows})
