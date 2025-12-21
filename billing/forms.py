from django import forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import Customer, Bill, BillItem, OldGold, Payment, GoldRate, SilverRate, BarRate
from decimal import Decimal


class LoginForm(AuthenticationForm):
    """Login form"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Login', css_class='btn btn-primary w-100')
        )


class CustomerForm(forms.ModelForm):
    """Customer form"""
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6'),
                Column('phone', css_class='form-group col-md-6'),
            ),
            'email',
            'address',
            Submit('submit', 'Save Customer', css_class='btn btn-primary')
        )


class GoldRateForm(forms.ModelForm):
    """Gold rate form"""
    class Meta:
        model = GoldRate
        fields = ['rate_24k']
        widgets = {
            'rate_24k': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'rate_24k',
            Submit('submit', 'Update Rate', css_class='btn btn-primary')
        )


class SilverRateForm(forms.ModelForm):
    """Silver rate form"""
    class Meta:
        model = SilverRate
        fields = ['rate_per_gram']
        widgets = {
            'rate_per_gram': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'rate_per_gram',
            Submit('submit', 'Update Rate', css_class='btn btn-primary')
        )


class BarRateForm(forms.ModelForm):
    """Bar rate form"""
    class Meta:
        model = BarRate
        fields = ['rate_per_gram']
        widgets = {
            'rate_per_gram': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'rate_per_gram',
            Submit('submit', 'Update Rate', css_class='btn btn-primary')
        )


class BillItemForm(forms.ModelForm):
    """Bill item form"""
    class Meta:
        model = BillItem
        fields = ['item_type', 'material_type', 'description', 'item_code', 'item_number', 'net_weight', 'tunch_wstg', 'labour', 'rate']
        widgets = {
            'item_type': forms.Select(attrs={'class': 'form-control'}),
            'material_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'item_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Code'}),
            'item_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Number (e.g., 5570)'}),
            'net_weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0.001'
            }),
            'tunch_wstg': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'max': '100'
            }),
            'rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'labour': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'value': '0.00'
            }),
        }


class OldGoldForm(forms.ModelForm):
    """Old gold exchange form"""
    class Meta:
        model = OldGold
        fields = ['weight', 'rate_per_gram', 'description']
        widgets = {
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0.001'
            }),
            'rate_per_gram': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('weight', css_class='form-group col-md-4'),
                Column('rate_per_gram', css_class='form-group col-md-4'),
                Column('description', css_class='form-group col-md-4'),
            ),
            Submit('submit', 'Add Old Gold', css_class='btn btn-warning')
        )


class BillForm(forms.ModelForm):
    """Bill form"""
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Bill
        fields = ['customer', 'cgst_percent', 'sgst_percent', 'cash_received', 'notes']
        widgets = {
            'cgst_percent': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'value': '1.50'
            }),
            'sgst_percent': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'value': '1.50'
            }),
            'cash_received': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If instance exists and has payments, set cash_received to sum of payments
        if self.instance and self.instance.pk and self.instance.payments.exists():
            total_payments = sum(p.amount for p in self.instance.payments.all())
            self.initial['cash_received'] = total_payments
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'customer',
            Row(
                Column('cgst_percent', css_class='form-group col-md-6'),
                Column('sgst_percent', css_class='form-group col-md-6'),
            ),
            'cash_received',
            'notes',
        )


class PaymentForm(forms.ModelForm):
    """Payment form"""
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method', 'notes']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        self.bill = kwargs.pop('bill', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('amount', css_class='form-group col-md-6'),
                Column('payment_method', css_class='form-group col-md-6'),
            ),
            'notes',
            Submit('submit', 'Add Payment', css_class='btn btn-success')
        )
    
    def clean_amount(self):
        """Validate payment amount doesn't exceed remaining balance"""
        amount = self.cleaned_data.get('amount', Decimal('0.00'))
        if self.bill:
            remaining_balance = self.bill.net_payable - self.bill.cash_received
            if amount > remaining_balance:
                raise forms.ValidationError(
                    f'Payment amount (₹{amount:,.2f}) cannot exceed remaining balance (₹{remaining_balance:,.2f}).'
                )
        if amount <= 0:
            raise forms.ValidationError('Payment amount must be greater than zero.')
        return amount


class BillSearchForm(forms.Form):
    """Bill search form"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by bill number or customer name...'
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Status')] + Bill.BILL_STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

