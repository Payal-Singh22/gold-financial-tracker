from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Gold Rate
    path('gold-rate/update/', views.update_gold_rate, name='update_gold_rate'),
    # Silver Rate
    path('silver-rate/update/', views.update_silver_rate, name='update_silver_rate'),
    # Bar Rate
    path('bar-rate/update/', views.update_bar_rate, name='update_bar_rate'),
    
    # Customers
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/update/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),
    
    # Bills
    path('bills/', views.BillListView.as_view(), name='bill_list'),
    path('bills/create/', views.bill_create, name='bill_create'),
    path('bills/<int:pk>/', views.BillDetailView.as_view(), name='bill_detail'),
    path('bills/<int:pk>/update/', views.bill_update, name='bill_update'),
    path('bills/<int:pk>/delete/', views.bill_delete, name='bill_delete'),
    path('bills/<int:pk>/print/', views.bill_print, name='bill_print'),
    path('bills/<int:pk>/pdf/', views.bill_pdf, name='bill_pdf'),
    path('bills/<int:pk>/email/', views.bill_email, name='bill_email'),
    path('bills/<int:bill_id>/payment/', views.add_payment, name='add_payment'),
    
    # Reports
    path('reports/', views.ReportsView.as_view(), name='reports'),
    path('api/create-customer/', views.create_customer_ajax, name='create_customer_ajax'),
]

