from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Customer(models.Model):
    """Customer model for storing customer information"""
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class GoldRate(models.Model):
    """Gold rate management - stores current gold rate"""
    rate_24k = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="24K Gold rate per gram"
    )
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_at']
        get_latest_by = 'updated_at'

    def __str__(self):
        return f"24K Gold: ₹{self.rate_24k}/gm"

    @classmethod
    def get_current_rate(cls):
        """Get the current active gold rate"""
        return cls.objects.filter(is_active=True).first()


class SilverRate(models.Model):
    """Silver rate management - stores current silver rate"""
    rate_per_gram = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Silver rate per gram"
    )
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_at']
        get_latest_by = 'updated_at'

    def __str__(self):
        return f"Silver: ₹{self.rate_per_gram}/gm"

    @classmethod
    def get_current_rate(cls):
        """Get the current active silver rate"""
        return cls.objects.filter(is_active=True).first()


class BarRate(models.Model):
    """Bar rate management - stores current bar rate"""
    rate_per_gram = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Bar rate per gram"
    )
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_at']
        get_latest_by = 'updated_at'

    def __str__(self):
        return f"Bar: ₹{self.rate_per_gram}/gm"

    @classmethod
    def get_current_rate(cls):
        """Get the current active bar rate"""
        return cls.objects.filter(is_active=True).first()


class Bill(models.Model):
    """Bill model for storing bill information"""
    BILL_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('paid', 'Paid'),
        ('partial', 'Partial'),
        ('unpaid', 'Unpaid'),
    ]

    bill_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bills')
    bill_date = models.DateTimeField(auto_now_add=True)
    gold_rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # Shop details (can be configured in settings)
    shop_name = models.CharField(max_length=200, default='ROHTASH SARRAF')
    shop_address = models.TextField(default='', blank=True)
    shop_gstin = models.CharField(max_length=15, blank=True, help_text="GSTIN number")
    
    # Balance fields
    ci_balance_gold = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.000'), help_text="CI Balance Gold")
    ci_balance_dr = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), help_text="CI Balance Dr")
    ci_balance_cr = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), help_text="CI Balance Cr")
    
    # Totals
    total_fine_gold = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.000'))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    
    # Old gold exchange
    old_gold_weight = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.000'))
    old_gold_rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    old_gold_value = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    
    # Tax
    cgst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('1.50'))
    sgst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('1.50'))
    cgst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    sgst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    
    # Final amounts
    net_payable = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    cash_received = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    
    status = models.CharField(max_length=20, choices=BILL_STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.bill_number} - {self.customer.name}"

    def calculate_totals(self):
        """Calculate all totals for the bill"""
        # Calculate total fine gold and amount from items
        items = self.items.all()
        self.total_fine_gold = sum(item.g_fine for item in items)
        self.total_amount = sum(item.amount for item in items)
        
        # Calculate tax
        taxable_amount = self.total_amount - self.old_gold_value
        self.cgst_amount = (taxable_amount * self.cgst_percent) / 100
        self.sgst_amount = (taxable_amount * self.sgst_percent) / 100
        
        # Calculate net payable
        self.net_payable = self.total_amount + self.cgst_amount + self.sgst_amount - self.old_gold_value
        
        # Calculate balance
        self.balance = self.net_payable - self.cash_received
        
        # Update status
        if self.balance <= 0:
            self.status = 'paid'
        elif self.cash_received > 0:
            self.status = 'partial'
        else:
            self.status = 'unpaid'
        
        self.save()

    def save(self, *args, **kwargs):
        if not self.bill_number:
            # Generate bill number
            from datetime import datetime
            date_str = datetime.now().strftime('%Y%m%d')
            last_bill = Bill.objects.filter(bill_number__startswith=f'JB{date_str}').order_by('-bill_number').first()
            if last_bill:
                try:
                    num = int(last_bill.bill_number.split('-')[-1]) + 1
                except:
                    num = 1
            else:
                num = 1
            self.bill_number = f'JB{date_str}-{num:03d}'
        super().save(*args, **kwargs)


class BillItem(models.Model):
    """Bill items model for storing individual items in a bill"""
    ITEM_TYPE_CHOICES = [
        ('S', 'S - New Gold'),
        ('REC', 'REC - Received Old Gold'),
    ]
    
    MATERIAL_TYPE_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bar', 'Bar'),
    ]
    
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES, default='S')
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPE_CHOICES, default='gold', help_text="Material type: Gold, Silver, or Bar")
    description = models.CharField(max_length=200)
    item_code = models.CharField(max_length=50, blank=True, help_text="Item code/SKU")
    item_number = models.CharField(max_length=20, blank=True, help_text="Item number (e.g., 5570, 5560)")
    net_weight = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        help_text="Net weight in grams"
    )
    tunch_wstg = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=Decimal('91.60'),
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Tunch wastage percentage (e.g., 78.00, 89.00)"
    )
    labour = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal('0.00'),
        help_text="Labour charges"
    )
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('7000.00'), help_text="Rate per gram")
    s_fine = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.000'), help_text="SFine")
    g_fine = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.000'), help_text="GFine (Gold Fine)")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.bill.bill_number} - {self.description}"

    def calculate_fines(self):
        """Calculate GFine: Net weight × Tunch wstg / 100"""
        self.g_fine = (self.net_weight * self.tunch_wstg) / 100
        # SFine can be same as GFine or calculated differently based on business logic
        self.s_fine = self.g_fine
        return self.g_fine

    def calculate_amount(self):
        """Calculate amount: (GFine × Rate) + Labour"""
        gold_amount = self.g_fine * self.rate
        self.amount = gold_amount + self.labour
        return self.amount

    def save(self, *args, **kwargs):
        self.calculate_fines()
        self.calculate_amount()
        super().save(*args, **kwargs)
        # Recalculate bill totals
        if self.bill:
            self.bill.calculate_totals()


class OldGold(models.Model):
    """Old gold exchange model"""
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='old_gold_exchanges')
    weight = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))]
    )
    rate_per_gram = models.DecimalField(max_digits=10, decimal_places=2)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Old Gold - {self.bill.bill_number}"

    def save(self, *args, **kwargs):
        self.value = self.weight * self.rate_per_gram
        super().save(*args, **kwargs)
        # Update bill old gold totals
        if self.bill:
            total_old_gold = sum(og.weight for og in self.bill.old_gold_exchanges.all())
            total_old_gold_value = sum(og.value for og in self.bill.old_gold_exchanges.all())
            self.bill.old_gold_weight = total_old_gold
            self.bill.old_gold_value = total_old_gold_value
            self.bill.calculate_totals()


class Payment(models.Model):
    """Payment model for tracking payments"""
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
    ]

    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    payment_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f"Payment of ₹{self.amount} for {self.bill.bill_number}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update bill cash received from sum of all payments
        if self.bill:
            total_payments = sum(p.amount for p in self.bill.payments.all())
            self.bill.cash_received = total_payments
            # Calculate totals (which also updates balance and status)
            self.bill.calculate_totals()
            # Save the bill with updated values
            self.bill.save(update_fields=['cash_received', 'balance', 'status', 'updated_at'])

