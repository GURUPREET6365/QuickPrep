from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Questions
from .question_gen import question_generator
from Notes.models import File
from django.contrib.auth.models import User

# Create your views here.
@login_required
def questionGenerator(request, pk):
    if request.method == 'POST':
        user = request.user # It returns the full object of the user with full information
        question_type = request.POST.get('type_question')
        question_num = request.POST.get('question_num')
        print('Trying to generate the question......')
        try:

            question_object = question_generator(pk, question_type, question_num)
        

            print('Saving the question to the database.')

            for all_question in question_object:
                # only_question = all_question.question 
                """
                We can not do this like that because the data is in dictionary and it has no any dot feature for accessing.
                """
                only_question = all_question['question']
                A = all_question['A']
                B = all_question['B']
                C = all_question['C']
                D = all_question['D']
                answer = all_question['answer']
                
                question = Questions.objects.create(
                    file = get_object_or_404(File, id=pk),
                    user = get_object_or_404(User, id = user.id),
                    question = only_question,
                    A = A,
                    B = B,
                    C = C,
                    D = D,
                    answer = answer
                )
                print('Question has been saved to the database.....')
        except Exception as e:
            print('The error is :', e)
        print('Returning to the question page.')
        return redirect('question-page')


from collections import defaultdict
"""
This is the default python library which is used to create the dictionary over the list, in which the key are created automatically as we give the value.
"""

@login_required
def question_page(request):
    user = request.user
    questions = Questions.objects.filter(user=user).order_by('-created_at')
    print('question type is:', type(questions))

    print('Now iterating questions.')
    date_and_id_dict = defaultdict(list)
    """
    This is uses list that tells if the key is empty return [] or if key is not present returns []

    It's format will be
    
    {
    (file_id, date):[list of question]
    }
    """

    """
    my_dict = {}
    my_dict["language"] = "Python"
    my_dict["level"] = "Beginner"

    The above is the method to add the value, in the dictionary.
    """
    for question in questions:
        date_only = question.created_at        
        key = (question.file_id, date_only)
        date_and_id_dict[key].append(question)

    # We will convert the date_and_id_dict into a list from a dictionary, which will be used better to get the data from grouped tuples.

    grouped_question = list(date_and_id_dict.items())

    """
    .items() converts a dictionary into key–value pairs, and list() turns them into a list of tuples.

    It's format will be:
        dict_items[
            ((file_id, date), [question list]),
            ((file_id, date), [question list])
        ]
    """

    return render(request, 'Test_Practise/generated_que_page.html', {'grouped_questions':grouped_question,})



@login_required
def Test_question(request, file_id, date):
    user = request.user
    questions = Questions.objects.filter(user=user, file_id = file_id, created_at = date)
    
    return render(request, 'Test_Practise/question_test_page_analysis.html', {'questions':questions,})