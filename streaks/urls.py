from django.urls import path
from . import views

urlpatterns = [
    path('streaks/', views.show_streaks, name='streaks'),
    path('create/streaks/', views.create_streaks, name='create_streaks'),
    path('streak/details/<int:pk>/', views.streak_details, name='streak_details'),
    path('show/streaks/', views.show_streaks, name='show_streaks'),
    path('streak/update/<int:pk>/', views.streak_update, name='streak_update'),
    path('edit/streak/<int:pk>/', views.edit_streak, name= 'edit_streak'),
    path('delete/streak/<int:pk>/', views.delete_streak, name='delete_streak')
]
