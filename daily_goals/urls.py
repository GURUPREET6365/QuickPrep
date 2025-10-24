from django.urls import path
from . import views

urlpatterns = [
    path('create/dailygoals', views.create_dailygoals, name='create_dailygoals'),
    path('view/dailygoals', views.view_dailygoals, name='view_dailygoals'),
    path('complete/dailygoals/<int:pk>/', views.complete_dailygoals, name='complete_dailygoals'),
    path('edit/dailygoals/<int:pk>/', views.edit_dailygoals, name='edit_dailygoals'),
    path('detailed/dailygoals/<int:pk>/', views.detailed_dailygoals, name='detailed_dailygoals'),
    path('delete/dailygoals/<int:pk>/', views.delete_dailygoals, name='delete_dailygoals')
    
]
