from django.urls import path
from . import views

urlpatterns = [
        # This is for question generator.
    path('question-gen/<int:pk>', views.questionGenerator, name='question-gen'),

    # This is question generated page.
    path('AI-Practise/Question', views.question_page, name='question-page'),

    # This is for the showing the questions in test format or fully detailed.
    path('Question/<int:file_id>/<str:date>/', views.Test_question, name='detailed_question')
]