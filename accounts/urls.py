from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomPasswordChangeForm

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/',    views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),
    path('delete/',   views.delete_view,   name='delete_account'),
       # Use form_class parameter to specify your custom form
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url='/password-change/done/',
        form_class=CustomPasswordChangeForm  # Add this line
    ), name='password_change'),
    
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/profile.html'
    ), name='password_change_done'),
    path('profile/', views.profile, name='profile')
]