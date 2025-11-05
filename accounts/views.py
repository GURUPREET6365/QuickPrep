from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
import os
from dotenv import load_dotenv

load_dotenv()

from .forms import CustomUserCreationForm
from .tokens import email_verification_token
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            token = email_verification_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
 # Build activation link
            domain = get_current_site(request).domain
            protocol = 'https' if request.is_secure() else 'http'
            activation_link = f"{protocol}://{domain}/verify-email/{uid}/{token}/"
            
            # Prepare and send verification email
            mail_subject = 'Verify your email address'
            message = render_to_string('accounts/email_verification.html', {
                'user': user,
                'activation_link': activation_link,
            })
            
            email = EmailMessage(
                subject=mail_subject,
                body=message,
                from_email=os.getenv('DEFAULT_FROM_EMAIL'),  # Or use DEFAULT_FROM_EMAIL
                to=[user.email]
            )
            email.content_subtype = 'html'  # Send as HTML
            email.send()
            
            messages.success(
                request,
                f'Registration successful! A verification link has been sent to {user.email}. Please check your email (and spam folder) to activate your account.'
            )
            return redirect('login')  # Redirect to login page
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def verify_email_view(request, uidb64, token):
    try:
        # Decode the user ID
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist):
        user = None
    
    # Check if token is valid
    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True  # Activate the user
        user.save()
        messages.success(request, 'Your email has been verified! You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid or has expired. Please register again.')
        return redirect('register')

    

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
            'l_login':current_user.last_login,
            'date_joined':current_user.date_joined,          
        }
    
    return render(request, 'accounts/profile.html', {'user':user,})