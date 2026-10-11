from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Expense, Category, Budget
from .forms import ExpenseForm,CategoryForm, BudgetForm
from django.db.models import Sum
from datetime import date


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('expense_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

@login_required
def expense_add(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(user=request.user)
        return render(request, 'expenses/expense_form.html', {'form': form, 'title': 'Add expense'})

@login_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('expense_add')
    else:
        form = CategoryForm()
    return render(request, 'expenses/category_form.html', {'form': form})

@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense, user=request.user)
    return render(request, 'expenses/expense_form.html', {'form': form, 'title': 'Edit expense', 'expense': expense})

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'expenses/expense_delete.html', {'expense': expense})

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    categories = Category.objects.filter(user=request.user)

    category_id = request.GET.get('category')
    start = request.GET.get('start')
    end = request.GET.get('end')
    q = request.GET.get('q')

    if category_id:
        expenses = expenses.filter(category_id=category_id)
    if start:
        expenses = expenses.filter(date__gte=start)
    if end:
        expenses = expenses.filter(date__lte=end)
    if q:
        expenses = expenses.filter(note__icontains=q)

    total = expenses.aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses,
        'categories': categories,
        'total': total,
    })

@login_required
def summary(request):
    today = date.today()
    ym = request.GET.get('ym') or today.strftime('%Y-%m')
    year, month = map(int, ym.split('-'))

    expenses = Expense.objects.filter(user=request.user, date__year=year, date__month=month)
    by_category = expenses.values('category__name').annotate(total=Sum('amount')).order_by('-total')
    total = expenses.aggregate(total=Sum('amount'))['total'] or 0

    labels = [row['category__name'] or 'Uncategorized' for row in by_category]
    values = [float(row['total']) for row in by_category]

    budget = Budget.objects.filter(user=request.user, month__year=year, month__month=month).first()
    status = None
    remaining = None
    percent = None
    if budget:
        remaining = budget.limit - total
        percent = int(total * 100 / budget.limit)
        if total > budget.limit:
            status = 'over'
        elif percent >= 80:
            status = 'near'
        else:
            status = 'ok'

    return render(request, 'expenses/summary.html', {
        'ym': ym, 'total': total, 'by_category': by_category,
        'labels': labels, 'values': values,
        'budget': budget, 'remaining': remaining,
        'percent': percent, 'status': status,
    })

@login_required
def budget_set(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            year, month = map(int, form.cleaned_data['month'].split('-'))
            Budget.objects.update_or_create(
                user=request.user,
                month=date(year, month, 1),
                defaults={'limit': form.cleaned_data['limit']},
            )
            return redirect('summary')
    else:
        form = BudgetForm()
    return render(request, 'expenses/budget_form.html', {'form': form})