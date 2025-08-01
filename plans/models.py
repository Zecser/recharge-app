from django.db import models
from decimal import Decimal, ROUND_HALF_UP
class Provider(models.Model):
    title = models.CharField(max_length=100)
    discount_percentage = models.PositiveIntegerField(null=True, blank=True, help_text="Optional discount (%) to apply to all its plans")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class Plans(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='plans')
    title = models.CharField(max_length=200)
    description = models.TextField()
    validity = models.IntegerField(help_text='Validity in days')
    is_active = models.BooleanField(default=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    identifier = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Plans'
        ordering = ['created_at']
    

    @property
    def final_price(self):
        if self.provider.discount_percentage:
            discount_percentage = Decimal(self.provider.discount_percentage) / Decimal('100')
            discount = self.amount * discount_percentage
            return (self.amount - discount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return self.amount
    def __str__(self):
        return f"{self.provider.title} - {self.title}"
