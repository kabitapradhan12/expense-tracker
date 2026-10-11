from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('register/', views.register, name='register'),
    path('add/', views.expense_add, name='expense_add'),
    path('categories/add/', views.category_add, name='category_add'),
    path('edit/<int:pk>/', views.expense_edit, name='expense_edit'),
    path('delete/<int:pk>/', views.expense_delete, name='expense_delete'),
    path('summary/', views.summary, name='summary'),
    path('budget/', views.budget_set, name='budget_set'),
] 