from django.shortcuts import render, get_object_or_404, redirect
# Here i am importing the Streak table from streaks app model file
from streaks.models import Streak
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from daily_goals.models import UsersGoals
from .models import ultimateGoal
from django.contrib import messages
from .forms import UltimateGoalForm

# Create your views here.
@login_required
def home(request):
    #  it creates a queryset limited to rows where the Streak.user foreign key equals the current request.user only.  It is equivalent to “SELECT … FROM streaks WHERE user_id = current_user_id”
    # streaks = Streak.objects.filter(user=request.user) request.user represents an AnonymousUser object. This object does not have a primary key (pk) or id attribute, as it doesn't correspond to a specific user in the database.
    ultimate_goal = ultimateGoal.objects.filter(user_id=request.user.id)
    ult_goal_list = []
    for ult_goal in ultimate_goal:
        ult_goal_list.append(ult_goal)


    today = timezone.localdate() 
    incomplete_goal = []
    goals = UsersGoals.objects.filter(user_id=request.user.id)
    for i_goal in goals:
        if not i_goal.completed:  # Checks if the goal is not completed (i.e., goal.completed is False)
            incomplete_goal.append(i_goal) 


    incomplete_streaks = []
    streaks = Streak.objects.filter(user_id=request.user.id)
    for i_streaks in streaks:
        if i_streaks.last_completed != today:
            incomplete_streaks.append(i_streaks)
            
    return render(request, 'home/home.html', {'streaks':streaks, 'incomplete_streaks':incomplete_streaks, 'incomplete_goal':incomplete_goal, 'goals':goals, 'ult_goal_list':ult_goal_list, 'ultimate_goal':ultimate_goal})


def about_us(request):
    return render(request, 'home/about_us.html')

@login_required
def ultimategoal(request):
    updated_date = timezone.localdate()
    if request.method == 'POST':
        title = request.POST.get('title')
        
        ultgoal = ultimateGoal.objects.create(
            user = request.user,
            title=title, 
            updated_at = updated_date
        )
        messages.info(request, 'The ultimate goal has been created.')
    return render(request, 'home/ultimategoal.html')


def edit_ultimate_goal(request):
    goal = ultimateGoal.objects.get(user=request.user)  # 👈 fetch via OneToOne

    if request.method == 'POST':
        form = UltimateGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your Ultimate Goal has been saved successfully')
            return redirect('home')
          # redirect wherever needed
    else:
        form = UltimateGoalForm(instance=goal)  # 👈 prefill form

    return render(request, 'home/editultimategoal.html', {'form': form})