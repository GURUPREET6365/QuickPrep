from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/us/', views.about_us, name='about_us'), 
    path('ultimate/goal/', views.ultimategoal, name='ultimategoal'),
    path('edit/ultimate/goal/', views.edit_ultimate_goal, name='editultimategoal'),
    path('delete/ultimate/goal', views.deleteultimategoal, name='deleteultimategoal')
]

