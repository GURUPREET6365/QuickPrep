from django.shortcuts import render

# Here i am importing the Streak table from streaks app model file
from streaks.models import Streak
from django.utils import timezone
from daily_goals.models import UsersGoals

# Create your views here.
def home(request):
    #  it creates a queryset limited to rows where the Streak.user foreign key equals the current request.user only.  It is equivalent to “SELECT … FROM streaks WHERE user_id = current_user_id”
    # streaks = Streak.objects.filter(user=request.user) request.user represents an AnonymousUser object. This object does not have a primary key (pk) or id attribute, as it doesn't correspond to a specific user in the database.
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
            
    return render(request, 'home/home.html', {'streaks':streaks, 'incomplete_streaks':incomplete_streaks, 'incomplete_goal':incomplete_goal, 'goals':goals})


def about_us(request):
    return render(request, 'home/about_us.html')