from django import forms
from .models import Expense, Category



class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'note']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class BudgetForm(forms.Form):
    month = forms.CharField(widget=forms.TextInput(attrs={'type': 'month'}))
    limit = forms.DecimalField(max_digits=10, decimal_places=2, min_value=1)