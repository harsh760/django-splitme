from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.db import connection
from django.contrib.auth.models import User
from django.db import OperationalError
import django.db



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    
def search(request):
    c_user = request.user
    if request.method == 'POST':
        if request.POST.get('search_now') != '':
            try:
                cursor = connection.cursor()
                search_name = request.POST['search_now']
                cursor.execute(
                    f"SELECT a.* , p.image from auth_user a, users_profile p where (a.id = p.user_id) and (a.first_name = '{search_name}' or a.last_name = '{search_name}' or a.username = '{search_name}')  and a.is_superuser = 0 and NOT a.id = {c_user.id}; ")
                
                ans = dictfetchall(cursor)
                # print(ans)

            finally:
                cursor.close()
            context ={
                'user_search':ans
            }
            if len(ans) == 0:
                messages.info(request, f'No data of {search_name} returned!')
                return render(request, 'users/search.html')
            else:   
                return render(request, 'users/search.html', context)
        else:
            return render(request, 'blog/home.html')
    return render(request, 'users/search.html')


def addFriends(request, uid):
    c_user = request.user
    try:
        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO `friends`(`u_id1`, `u_id2`) VALUES ({c_user.id},{uid}); ")

    except OperationalError as e:
        (error_code, msg) = e.args 
        messages.info(request, msg)     

    finally:
        cursor.close()

    return redirect('search')


