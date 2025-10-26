from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# Create your views here.
def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username  = request.POST.get('username')
        email     = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken use different one.')
            return redirect('register')
        
        elif not email:
            messages.error(request, 'Email is required!')

        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken use different one.')
            return redirect('register')
        # Create and save new user
        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password1,
                                        first_name=first_name,
                                        last_name=last_name)
        user.save()
        messages.success(request, 'Registration successful')
        login(request, user)
        return redirect('home')

    else:
        return render(request, 'accounts/register.html')




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,
                            username=username,
                            password=password)
        if user is not None:
            #login(request, user): This function, also from django.contrib.auth, is crucial for establishing the user's session. It takes the request object and the authenticated user object as arguments. Its primary role is to set up the user's session in Django's authentication system, marking them as logged in. This includes storing the user's ID in the session, which allows Django to recognize the user on subsequent requests.
            messages.success(request, 'Logged in successful')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


@login_required
def logout_view(request): 
    #logout(request) clears all session data for this request and removes the authentication state, and it is safe even if the user was not logged in
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('home')



@login_required
def delete_view(request):
    if request.method == 'POST':
        request.user.delete()
        messages.info(request, 'Account deleted.')
        return redirect('home')
    else:
        return render(request, 'accounts/delete.html')

@login_required
def profile(request):
    # user_id = User.objects.filter(user_id=request.user)
    # The request.user object already contains the logged-in user's data
    current_user = request.user

    user={'username':current_user.username,
            'f_name':current_user.first_name,
            'l_name':current_user.last_name,
            'email':current_user.email,                 
        }
    
    return render(request, 'accounts/profile.html', {'user':user,})