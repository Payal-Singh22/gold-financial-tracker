"""
Signals for auto-calculations and model updates
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Bill, BillItem, OldGold, Payment


@receiver(post_save, sender=BillItem)
def update_bill_on_item_save(sender, instance, **kwargs):
    """Recalculate bill totals when item is saved"""
    if instance.bill:
        instance.bill.calculate_totals()


@receiver(post_save, sender=OldGold)
def update_bill_on_old_gold_save(sender, instance, **kwargs):
    """Recalculate bill totals when old gold is saved"""
    if instance.bill:
        # Update bill old gold totals
        total_old_gold = sum(og.weight for og in instance.bill.old_gold_exchanges.all())
        total_old_gold_value = sum(og.value for og in instance.bill.old_gold_exchanges.all())
        instance.bill.old_gold_weight = total_old_gold
        instance.bill.old_gold_value = total_old_gold_value
        instance.bill.calculate_totals()


@receiver(post_save, sender=Payment)
def update_bill_on_payment_save(sender, instance, **kwargs):
    """Recalculate bill totals when payment is saved"""
    if instance.bill:
        # Update bill cash received
        total_payments = sum(p.amount for p in instance.bill.payments.all())
        instance.bill.cash_received = total_payments
        instance.bill.calculate_totals()

