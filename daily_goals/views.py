from django.shortcuts import render, redirect, get_object_or_404
from .models import UsersGoals
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .forms import EditGoalForm
from django.contrib import messages

# Create your views here.
@login_required
def create_dailygoals(request):
    created_date = timezone.localdate()
    if request.method == "POST":
        # Form data nikal lo
        title = request.POST.get('title')
        description = request.POST.get('description')
        action = request.POST.get('action')  # ye "create_ones" ya "create_many" hoga
        
        # Goal create karo
        goal = UsersGoals.objects.create(
            user=request.user,
            title=title,
            description=description,
            completed=False,
            updated_at=created_date
        )
        
        # Check karo kon sa button click hua
        if action == 'create_ones':
            # Single goal create hua, list page pe redirect
            return redirect('view_dailygoals')  # ya jo bhi tumhara list view ka name hai
        
        elif action == 'create_many':
            # Multiple goals create karna hai, form page pe wapas aao
            return redirect('create_dailygoals')  # Same page reload hoga
    
    # GET request par form dikhao
    return render(request, 'daily_goals/create_dailygoals.html')


@login_required
def view_dailygoals(request):
    user_goal = UsersGoals.objects.filter(
        user=request.user
    )
    today = timezone.localdate()
    all_goal=[]
    for goals in user_goal:
        created_date = timezone.localdate(goals.created_at)
        deadline_date = created_date + timedelta(days=1)
         # below are the two boolean checkng statement that check and return true or false.
        done = (goals.completed)
        can_complete = (today <= deadline_date) and (not goals.completed)
        cannot_complete = (today > deadline_date) and (not goals.completed)
        all_goal.append(
            {
                'goal': goals,
                'can_complete':can_complete,
                'cannot_complete':cannot_complete,
                'done_goal':done
            }
        )

    return render(request, 'daily_goals/view_dailygoals.html', {'all_goal':all_goal})


@login_required
def complete_dailygoals(request, pk):

    goal = get_object_or_404(UsersGoals, pk=pk, user=request.user)
    if request.method != 'POST':
        return redirect('view_dailygoals')
    if request.method=='POST':
        goal.is_active=False
        goal.completed=True
        goal.save()
        return redirect('view_dailygoals')
    
@login_required
def edit_dailygoals(request, pk):
    today = timezone.localdate()
    goal = get_object_or_404(UsersGoals, pk=pk, user=request.user)

    if request.method == 'POST':
        form = EditGoalForm(request.POST, instance=goal)  # Bind POST data to instance
        if form.is_valid():
            goal.updated_at=today
            form.save()  # ModelForm saves to goal automatically
            messages.success(request, 'Goals Updated')
            return redirect('view_dailygoals')  # Redirect after success (PRG pattern)
    else:

        form = EditGoalForm(instance=goal)  # Prefill with current goal data on GET

    return render(request, 'daily_goals/edit_dailygoals.html', {'form': form, 'goal': goal})


def detailed_dailygoals(request, pk):
    goal = get_object_or_404(UsersGoals, pk=pk, user=request.user)
    return render(request, 'daily_goals/detailed_dailygoals.html', {'goal':goal,})

def delete_dailygoals(request, pk):
    goal = get_object_or_404(UsersGoals, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        return redirect('view_dailygoals')
    return redirect('view_dailygoals')