# Generated migration to recalculate existing items

from django.db import migrations
from decimal import Decimal


def recalculate_items(apps, schema_editor):
    """Recalculate g_fine, s_fine, and amount for existing items"""
    BillItem = apps.get_model('billing', 'BillItem')
    
    for item in BillItem.objects.all():
        # Recalculate fines
        if item.net_weight and item.tunch_wstg:
            item.g_fine = (item.net_weight * item.tunch_wstg) / 100
            item.s_fine = item.g_fine
        
        # Recalculate amount
        if item.g_fine and item.rate:
            gold_amount = item.g_fine * item.rate
            item.amount = gold_amount + (item.labour or Decimal('0.00'))
        
        item.save(update_fields=['g_fine', 's_fine', 'amount'])


def reverse_recalculate(apps, schema_editor):
    """Reverse migration - no action needed"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0003_remove_billitem_fine_gold_and_more'),
    ]

    operations = [
        migrations.RunPython(recalculate_items, reverse_recalculate),
    ]

