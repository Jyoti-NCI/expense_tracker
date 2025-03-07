from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login
from .forms import RegisterForm
from .models import *
from .forms import *

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('expense_list')
    else:
        form = RegisterForm()
    return render(request, 'tracker_app/register.html', {'form': form})


def expense_list(request):
    expenses = Expense.objects.all()
    # print("expenses ====> ",expenses)
    return render(request, 'tracker_app/expense_list.html', {'expenses': expenses})

def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            # Assigning logged in user
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = ExpenseForm()
    return render(request, 'tracker_app/expense_form.html', {'form': form})

def update_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user, is_active=True)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            expense.author = request.user
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'tracker_app/expense_form.html', {'form': form})

# Delete expense
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user, is_active=True)
    if request.method == 'POST':
        expense.author = request.user
        expense.delete()
        return redirect('expense_list')
    return render(request, 'tracker_app/expense_confirm_delete.html', {'expense': expense})