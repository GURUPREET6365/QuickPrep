from django.urls import path
from . import views

urlpatterns = [
    path('streaks/', views.show_streaks, name='streaks'),
    path('create_streaks/', views.create_streaks, name='create_streaks'),
    path('streak_details/<int:pk>/', views.streak_details, name='streak_details'),
    path('show_streaks/', views.show_streaks, name='show_streaks'),
    path('streak_update/<int:pk>/', views.streak_update, name='streak_update'),
    path('edit_streak/<int:pk>/', views.edit_streak, name= 'edit_streak'),
    path('delete_streak/<int:pk>/', views.delete_streak, name='delete_streak')
]
