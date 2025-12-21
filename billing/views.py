from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum, Q, Count
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta
from decimal import Decimal
import json

from .models import Customer, Bill, BillItem, OldGold, Payment, GoldRate, SilverRate, BarRate
from .forms import (
    LoginForm, CustomerForm, GoldRateForm, SilverRateForm, BarRateForm, BillForm, 
    BillItemForm, OldGoldForm, PaymentForm, BillSearchForm
)
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError):
    WEASYPRINT_AVAILABLE = False
    HTML = None  # Define HTML as None when not available


class LoginView(TemplateView):
    """Login view"""
    template_name = 'billing/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        return render(request, self.template_name, {'form': form})


@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    return redirect('login')


class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard view"""
    template_name = 'billing/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current gold rate
        gold_rate = GoldRate.get_current_rate()
        context['gold_rate'] = gold_rate
        # Get current silver rate
        silver_rate = SilverRate.get_current_rate()
        context['silver_rate'] = silver_rate
        # Get current bar rate
        bar_rate = BarRate.get_current_rate()
        context['bar_rate'] = bar_rate
        
        # Today's date
        today = timezone.now().date()
        
        # Today's statistics
        today_bills = Bill.objects.filter(bill_date__date=today)
        context['today_total_sales'] = today_bills.aggregate(
            total=Sum('net_payable')
        )['total'] or Decimal('0.00')
        
        context['today_cash_received'] = today_bills.aggregate(
            total=Sum('cash_received')
        )['total'] or Decimal('0.00')
        
        # Calculate cash received percentage
        if context['today_total_sales'] > 0:
            context['cash_received_percentage'] = round(
                (context['today_cash_received'] / context['today_total_sales']) * 100, 
                1
            )
        else:
            context['cash_received_percentage'] = 0
        
        # Old gold received today
        today_old_gold = OldGold.objects.filter(
            bill__bill_date__date=today
        ).aggregate(
            total=Sum('weight')
        )['total'] or Decimal('0.000')
        context['today_gold_received'] = today_old_gold
        
        # Outstanding balance
        outstanding_bills = Bill.objects.filter(
            status__in=['unpaid', 'partial']
        )
        context['outstanding_balance'] = outstanding_bills.aggregate(
            total=Sum('balance')
        )['total'] or Decimal('0.00')
        context['outstanding_count'] = outstanding_bills.count()
        
        # Recent bills
        context['recent_bills'] = Bill.objects.all()[:10]
        
        # Yesterday comparison
        yesterday = today - timedelta(days=1)
        yesterday_bills = Bill.objects.filter(bill_date__date=yesterday)
        yesterday_sales = yesterday_bills.aggregate(
            total=Sum('net_payable')
        )['total'] or Decimal('0.00')
        
        if yesterday_sales > 0:
            growth = ((context['today_total_sales'] - yesterday_sales) / yesterday_sales) * 100
            context['sales_growth'] = round(growth, 1)
        else:
            context['sales_growth'] = 0
        
        return context


class CustomerListView(LoginRequiredMixin, ListView):
    """Customer list view"""
    model = Customer
    template_name = 'billing/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 20


class CustomerCreateView(LoginRequiredMixin, CreateView):
    """Customer create view"""
    model = Customer
    form_class = CustomerForm
    template_name = 'billing/customer_form.html'
    success_url = reverse_lazy('customer_list')


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    """Customer update view"""
    model = Customer
    form_class = CustomerForm
    template_name = 'billing/customer_form.html'
    success_url = reverse_lazy('customer_list')


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    """Customer delete view"""
    model = Customer
    template_name = 'billing/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')


@login_required
def update_gold_rate(request):
    """Update gold rate"""
    if request.method == 'POST':
        # Deactivate old rates
        GoldRate.objects.filter(is_active=True).update(is_active=False)
        
        # Get rate from POST data
        rate_24k = request.POST.get('rate_24k')
        if not rate_24k:
            # Try alternative field name
            rate_24k = request.POST.get('rate')
        
        if rate_24k:
            try:
                rate_value = Decimal(rate_24k)
                gold_rate = GoldRate.objects.create(
                    rate_24k=rate_value,
                    updated_by=request.user,
                    is_active=True
                )
                return JsonResponse({'success': True, 'rate': str(gold_rate.rate_24k)})
            except (ValueError, TypeError):
                return JsonResponse({'success': False, 'error': 'Invalid rate value'})
        
        return JsonResponse({'success': False, 'error': 'Rate not provided'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def update_silver_rate(request):
    """Update silver rate"""
    if request.method == 'POST':
        # Deactivate old rates
        SilverRate.objects.filter(is_active=True).update(is_active=False)
        
        # Get rate from POST data
        rate_per_gram = request.POST.get('rate_per_gram')
        if not rate_per_gram:
            # Try alternative field name
            rate_per_gram = request.POST.get('rate')
        
        if rate_per_gram:
            try:
                rate_value = Decimal(rate_per_gram)
                silver_rate = SilverRate.objects.create(
                    rate_per_gram=rate_value,
                    updated_by=request.user,
                    is_active=True
                )
                return JsonResponse({'success': True, 'rate': str(silver_rate.rate_per_gram)})
            except (ValueError, TypeError):
                return JsonResponse({'success': False, 'error': 'Invalid rate value'})
        
        return JsonResponse({'success': False, 'error': 'Rate not provided'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def update_bar_rate(request):
    """Update bar rate"""
    if request.method == 'POST':
        # Deactivate old rates
        BarRate.objects.filter(is_active=True).update(is_active=False)
        
        # Get rate from POST data
        rate_per_gram = request.POST.get('rate_per_gram')
        if not rate_per_gram:
            # Try alternative field name
            rate_per_gram = request.POST.get('rate')
        
        if rate_per_gram:
            try:
                rate_value = Decimal(rate_per_gram)
                bar_rate = BarRate.objects.create(
                    rate_per_gram=rate_value,
                    updated_by=request.user,
                    is_active=True
                )
                return JsonResponse({'success': True, 'rate': str(bar_rate.rate_per_gram)})
            except (ValueError, TypeError):
                return JsonResponse({'success': False, 'error': 'Invalid rate value'})
        
        return JsonResponse({'success': False, 'error': 'Rate not provided'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


class BillListView(LoginRequiredMixin, ListView):
    """Bill list view"""
    model = Bill
    template_name = 'billing/bill_list.html'
    context_object_name = 'bills'
    paginate_by = 20

    def get_queryset(self):
        queryset = Bill.objects.select_related('customer').all()
        form = BillSearchForm(self.request.GET)
        
        if form.is_valid():
            search = form.cleaned_data.get('search')
            status = form.cleaned_data.get('status')
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')
            
            if search:
                queryset = queryset.filter(
                    Q(bill_number__icontains=search) |
                    Q(customer__name__icontains=search)
                )
            
            if status:
                queryset = queryset.filter(status=status)
            
            if date_from:
                queryset = queryset.filter(bill_date__date__gte=date_from)
            
            if date_to:
                queryset = queryset.filter(bill_date__date__lte=date_to)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = BillSearchForm(self.request.GET)
        return context


@login_required
def bill_create(request):
    """Create bill view"""
    gold_rate = GoldRate.get_current_rate()
    silver_rate = SilverRate.get_current_rate()
    bar_rate = BarRate.get_current_rate()
    
    if request.method == 'POST':
        bill_form = BillForm(request.POST)
        
        if bill_form.is_valid():
            bill = bill_form.save(commit=False)
            bill.created_by = request.user
            if gold_rate:
                bill.gold_rate = gold_rate.rate_24k
            bill.save()
            
            # Handle bill items
            items_data = json.loads(request.POST.get('items', '[]'))
            for idx, item_data in enumerate(items_data):
                # Determine default rate based on material type
                material_type = item_data.get('material_type', 'gold')
                default_rate = str(bill.gold_rate)
                if material_type == 'silver' and silver_rate:
                    default_rate = str(silver_rate.rate_per_gram)
                elif material_type == 'bar' and bar_rate:
                    default_rate = str(bar_rate.rate_per_gram)
                
                BillItem.objects.create(
                    bill=bill,
                    item_type=item_data.get('item_type', 'S'),
                    material_type=material_type,
                    description=item_data.get('description', ''),
                    item_code=item_data.get('item_code', ''),
                    item_number=item_data.get('item_number', ''),
                    net_weight=Decimal(item_data.get('net_weight', '0')),
                    tunch_wstg=Decimal(item_data.get('tunch_wstg', '91.60')),
                    labour=Decimal(item_data.get('labour', '0')),
                    rate=Decimal(item_data.get('rate', default_rate)),
                    order=idx
                )
            
            # Handle old gold
            old_gold_data = json.loads(request.POST.get('old_gold', '[]'))
            for og_data in old_gold_data:
                OldGold.objects.create(
                    bill=bill,
                    weight=Decimal(og_data.get('weight', '0')),
                    rate_per_gram=Decimal(og_data.get('rate_per_gram', str(bill.gold_rate))),
                    description=og_data.get('description', '')
                )
            
            # Recalculate totals after items and old gold are saved
            bill.calculate_totals()
            
            # If payments exist, cash_received should be sum of payments, not form value
            if bill.payments.exists():
                total_payments = sum(p.amount for p in bill.payments.all())
                bill.cash_received = total_payments
                bill.calculate_totals()
            
            # Validate cash received doesn't exceed net payable
            if bill.cash_received > bill.net_payable:
                bill_form.add_error('cash_received', 
                    f'Cash received (₹{bill.cash_received:,.2f}) cannot exceed net payable (₹{bill.net_payable:,.2f}).')
                # Delete the bill and items if validation fails
                bill.delete()
                return render(request, 'billing/bill_create.html', {
                    'bill_form': bill_form,
                    'gold_rate': gold_rate,
                    'silver_rate': silver_rate,
                    'bar_rate': bar_rate,
                    'customers': Customer.objects.all(),
                })
            
            bill.save()  # Save again with updated totals
            return redirect('bill_detail', pk=bill.pk)
    else:
        bill_form = BillForm()
    
    context = {
        'bill_form': bill_form,
        'gold_rate': gold_rate,
        'silver_rate': silver_rate,
        'bar_rate': bar_rate,
        'customers': Customer.objects.all(),
    }
    return render(request, 'billing/bill_create.html', context)


class BillDetailView(LoginRequiredMixin, DetailView):
    """Bill detail view"""
    model = Bill
    template_name = 'billing/bill_detail.html'
    context_object_name = 'bill'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment_form'] = PaymentForm()
        
        # Recalculate any items that might have missing calculations
        for item in self.object.items.all():
            if (item.g_fine == 0 or item.s_fine == 0) and item.net_weight > 0 and item.tunch_wstg > 0:
                item.calculate_fines()
                item.calculate_amount()
                item.save(update_fields=['g_fine', 's_fine', 'amount'])
            if item.rate == 0 and self.object.gold_rate > 0:
                item.rate = self.object.gold_rate
                item.calculate_amount()
                item.save(update_fields=['rate', 'amount'])
        
        # Calculate subtotals by type for print view
        items_by_type = {}
        for item in self.object.items.all():
            if item.item_type not in items_by_type:
                items_by_type[item.item_type] = {'items': [], 'total_weight': Decimal('0.000'), 'total_gfine': Decimal('0.000')}
            items_by_type[item.item_type]['items'].append(item)
            items_by_type[item.item_type]['total_weight'] += item.net_weight
            items_by_type[item.item_type]['total_gfine'] += item.g_fine
        
        context['items_by_type'] = items_by_type
        return context


@login_required
def bill_update(request, pk):
    """Update bill view"""
    bill = get_object_or_404(Bill, pk=pk)
    
    if request.method == 'POST':
        bill_form = BillForm(request.POST, instance=bill)
        
        if bill_form.is_valid():
            # Save form but don't update cash_received if payments exist
            bill = bill_form.save(commit=False)
            
            # Store original cash_received if payments exist
            has_payments = bill.payments.exists()
            if has_payments:
                # Don't update cash_received from form if payments exist
                original_cash_received = sum(p.amount for p in bill.payments.all())
            else:
                # Use cash_received from form if no payments
                original_cash_received = bill_form.cleaned_data.get('cash_received', Decimal('0.00'))
            
            bill.save()
            
            # Update items
            items_data = json.loads(request.POST.get('items', '[]'))
            # Delete existing items
            bill.items.all().delete()
            # Get rates
            silver_rate = SilverRate.get_current_rate()
            bar_rate = BarRate.get_current_rate()
            # Create new items
            for idx, item_data in enumerate(items_data):
                # Determine default rate based on material type
                material_type = item_data.get('material_type', 'gold')
                default_rate = str(bill.gold_rate)
                if material_type == 'silver' and silver_rate:
                    default_rate = str(silver_rate.rate_per_gram)
                elif material_type == 'bar' and bar_rate:
                    default_rate = str(bar_rate.rate_per_gram)
                
                BillItem.objects.create(
                    bill=bill,
                    item_type=item_data.get('item_type', 'S'),
                    material_type=material_type,
                    description=item_data.get('description', ''),
                    item_code=item_data.get('item_code', ''),
                    item_number=item_data.get('item_number', ''),
                    net_weight=Decimal(item_data.get('net_weight', '0')),
                    tunch_wstg=Decimal(item_data.get('tunch_wstg', '91.60')),
                    labour=Decimal(item_data.get('labour', '0')),
                    rate=Decimal(item_data.get('rate', default_rate)),
                    order=idx
                )
            
            # Update old gold
            old_gold_data = json.loads(request.POST.get('old_gold', '[]'))
            bill.old_gold_exchanges.all().delete()
            for og_data in old_gold_data:
                OldGold.objects.create(
                    bill=bill,
                    weight=Decimal(og_data.get('weight', '0')),
                    rate_per_gram=Decimal(og_data.get('rate_per_gram', str(bill.gold_rate))),
                    description=og_data.get('description', '')
                )
            
            # Recalculate totals after items and old gold are saved
            bill.calculate_totals()
            
            # Set cash_received: use sum of payments if payments exist, otherwise use form value
            if has_payments:
                bill.cash_received = sum(p.amount for p in bill.payments.all())
            else:
                bill.cash_received = original_cash_received
            
            # Recalculate balance and status
            bill.calculate_totals()
            
            # Validate cash received doesn't exceed net payable
            if bill.cash_received > bill.net_payable:
                bill_form.add_error('cash_received', 
                    f'Cash received (₹{bill.cash_received:,.2f}) cannot exceed net payable (₹{bill.net_payable:,.2f}).')
                return render(request, 'billing/bill_update.html', {
                    'bill': bill,
                    'bill_form': bill_form,
                    'gold_rate': GoldRate.get_current_rate(),
                    'silver_rate': SilverRate.get_current_rate(),
                    'bar_rate': BarRate.get_current_rate(),
                    'customers': Customer.objects.all(),
                })
            
            bill.save()  # Save again with updated totals
            return redirect('bill_detail', pk=bill.pk)
    else:
        bill_form = BillForm(instance=bill)
    
    # Recalculate any items that might have missing calculations
    for item in bill.items.all():
        if (item.g_fine == 0 or item.s_fine == 0) and item.net_weight > 0 and item.tunch_wstg > 0:
            item.calculate_fines()
            item.calculate_amount()
            item.save(update_fields=['g_fine', 's_fine', 'amount'])
        if item.rate == 0 and bill.gold_rate > 0:
            item.rate = bill.gold_rate
            item.calculate_amount()
            item.save(update_fields=['rate', 'amount'])
    
    # Recalculate bill totals to ensure they're correct
    bill.calculate_totals()
    
    # If payments exist, set cash_received to sum of payments for display
    if bill.payments.exists():
        total_payments = sum(p.amount for p in bill.payments.all())
        # Update the form instance to show correct cash_received
        bill_form.initial['cash_received'] = total_payments
        bill.cash_received = total_payments
        bill.calculate_totals()
        bill.save(update_fields=['cash_received', 'balance', 'status'])
    else:
        # If no payments, use the current cash_received value
        bill_form.initial['cash_received'] = bill.cash_received
    
    context = {
        'bill': bill,
        'bill_form': bill_form,
        'gold_rate': GoldRate.get_current_rate(),
        'silver_rate': SilverRate.get_current_rate(),
        'bar_rate': BarRate.get_current_rate(),
        'customers': Customer.objects.all(),
    }
    return render(request, 'billing/bill_update.html', context)


@login_required
def bill_delete(request, pk):
    """Delete bill view"""
    bill = get_object_or_404(Bill, pk=pk)
    if request.method == 'POST':
        bill.delete()
        return redirect('bill_list')
    return render(request, 'billing/bill_confirm_delete.html', {'bill': bill})


@login_required
def add_payment(request, bill_id):
    """Add payment to bill"""
    bill = get_object_or_404(Bill, pk=bill_id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, bill=bill)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.bill = bill
            payment.created_by = request.user
            payment.save()
            # Payment.save() method already updates bill.cash_received and calls calculate_totals()
            # So we just need to refresh the bill from DB to get updated values
            bill.refresh_from_db()
            return redirect('bill_detail', pk=bill.pk)
        else:
            # Return to bill detail with form errors
            return redirect('bill_detail', pk=bill.pk)
    
    return redirect('bill_detail', pk=bill.pk)


@login_required
def bill_print(request, pk):
    """Print bill view"""
    bill = get_object_or_404(Bill, pk=pk)
    
    # Recalculate any items that might have missing calculations
    for item in bill.items.all():
        if (item.g_fine == 0 or item.s_fine == 0) and item.net_weight > 0 and item.tunch_wstg > 0:
            item.calculate_fines()
            item.calculate_amount()
            item.save(update_fields=['g_fine', 's_fine', 'amount'])
        if item.rate == 0 and bill.gold_rate > 0:
            item.rate = bill.gold_rate
            item.calculate_amount()
            item.save(update_fields=['rate', 'amount'])
    
    # Calculate subtotals by type
    items_by_type = {}
    for item in bill.items.all():
        if item.item_type not in items_by_type:
            items_by_type[item.item_type] = {'items': [], 'total_weight': Decimal('0.000'), 'total_gfine': Decimal('0.000')}
        items_by_type[item.item_type]['items'].append(item)
        items_by_type[item.item_type]['total_weight'] += item.net_weight
        items_by_type[item.item_type]['total_gfine'] += item.g_fine
    
    return render(request, 'billing/bill_print.html', {
        'bill': bill,
        'items_by_type': items_by_type
    })


@login_required
def bill_pdf(request, pk):
    """Generate PDF for bill"""
    bill = get_object_or_404(Bill, pk=pk)
    
    if not WEASYPRINT_AVAILABLE:
        return HttpResponse(
            "PDF generation requires WeasyPrint with GTK3 runtime. "
            "Please install GTK3 runtime or use the print function instead.",
            content_type='text/plain',
            status=503
        )
    
    html_string = render_to_string('billing/bill_pdf.html', {'bill': bill})
    
    # Generate PDF
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf_file = html.write_pdf()
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill_{bill.bill_number}.pdf"'
    return response


@login_required
def create_customer_ajax(request):
    """Create customer via AJAX for bill form"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            name = data.get('name', '').strip()
            phone = data.get('phone', '').strip()
            email = data.get('email', '').strip()
            address = data.get('address', '').strip()
            
            # Validation
            if not name or not phone:
                return JsonResponse({
                    'success': False,
                    'error': 'Name and Phone are required fields.'
                }, status=400)
            
            # Check if customer with same phone already exists
            if Customer.objects.filter(phone=phone).exists():
                existing = Customer.objects.get(phone=phone)
                return JsonResponse({
                    'success': False,
                    'error': f'Customer with phone {phone} already exists: {existing.name}'
                }, status=400)
            
            # Create customer
            customer = Customer.objects.create(
                name=name,
                phone=phone,
                email=email if email else '',
                address=address if address else ''
            )
            
            return JsonResponse({
                'success': True,
                'customer': {
                    'id': customer.id,
                    'name': customer.name,
                    'phone': customer.phone,
                    'email': customer.email
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)


@login_required
def bill_email(request, pk):
    """Email bill as PDF"""
    bill = get_object_or_404(Bill, pk=pk)
    
    if not bill.customer.email:
        return JsonResponse({'success': False, 'error': 'Customer email not found'})
    
    if not WEASYPRINT_AVAILABLE:
        return JsonResponse({
            'success': False, 
            'error': 'PDF generation requires WeasyPrint with GTK3 runtime. Please install GTK3 runtime.'
        })
    
    # Recalculate any items that might have missing calculations
    for item in bill.items.all():
        if (item.g_fine == 0 or item.s_fine == 0) and item.net_weight > 0 and item.tunch_wstg > 0:
            item.calculate_fines()
            item.calculate_amount()
            item.save(update_fields=['g_fine', 's_fine', 'amount'])
    
    # Calculate subtotals by type
    items_by_type = {}
    for item in bill.items.all():
        if item.item_type not in items_by_type:
            items_by_type[item.item_type] = {'items': [], 'total_weight': Decimal('0.000'), 'total_gfine': Decimal('0.000')}
        items_by_type[item.item_type]['items'].append(item)
        items_by_type[item.item_type]['total_weight'] += item.net_weight
        items_by_type[item.item_type]['total_gfine'] += item.g_fine
    
    # Generate PDF
    html_string = render_to_string('billing/bill_pdf.html', {
        'bill': bill,
        'items_by_type': items_by_type
    })
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf_file = html.write_pdf()
    
    # Create email
    email = EmailMessage(
        subject=f'Bill {bill.bill_number} - {bill.customer.name}',
        body=f'Please find attached bill {bill.bill_number} for {bill.customer.name}.',
        from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@jewellerybilling.com',
        to=[bill.customer.email],
    )
    email.attach(f'bill_{bill.bill_number}.pdf', pdf_file, 'application/pdf')
    email.send()
    
    return JsonResponse({'success': True, 'message': 'Bill sent successfully'})


class ReportsView(LoginRequiredMixin, TemplateView):
    """Reports view"""
    template_name = 'billing/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Date range
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        
        if date_from and date_to:
            bills = Bill.objects.filter(
                bill_date__date__gte=date_from,
                bill_date__date__lte=date_to
            )
        else:
            # Default to current month
            today = timezone.now().date()
            bills = Bill.objects.filter(
                bill_date__date__year=today.year,
                bill_date__date__month=today.month
            )
        
        context['bills'] = bills
        context['total_sales'] = bills.aggregate(total=Sum('net_payable'))['total'] or Decimal('0.00')
        context['total_cash'] = bills.aggregate(total=Sum('cash_received'))['total'] or Decimal('0.00')
        context['total_outstanding'] = bills.filter(status__in=['unpaid', 'partial']).aggregate(
            total=Sum('balance')
        )['total'] or Decimal('0.00')
        context['bill_count'] = bills.count()
        
        return context

