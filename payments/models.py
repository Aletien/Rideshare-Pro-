from django.db import models
from users.models import User
from rides.models import Ride

class PaymentMethod(models.Model):
    METHOD_CHOICES = (
        ('card', 'Credit/Debit Card'),
        ('wallet', 'Wallet'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    method_type = models.CharField(max_length=20, choices=METHOD_CHOICES)
    
    # Card details (encrypted in production)
    card_last_four = models.CharField(max_length=4, blank=True)
    card_brand = models.CharField(max_length=50, blank=True)
    
    # Wallet
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.method_type}"


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('payment', 'Payment'),
        ('refund', 'Refund'),
        ('wallet_topup', 'Wallet Top-up'),
        ('withdrawal', 'Withdrawal'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    ride = models.ForeignKey(Ride, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    
    stripe_transaction_id = models.CharField(max_length=255, blank=True, unique=True)
    reference_number = models.CharField(max_length=100, unique=True)
    
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Transaction #{self.reference_number} - {self.amount}"


class Invoice(models.Model):
    ride = models.OneToOneField(Ride, on_delete=models.CASCADE, related_name='invoice')
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='invoice')
    
    base_fare = models.DecimalField(max_digits=10, decimal_places=2)
    distance_charge = models.DecimalField(max_digits=10, decimal_places=2)
    time_charge = models.DecimalField(max_digits=10, decimal_places=2)
    surge_multiplier = models.FloatField(default=1.0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    issued_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Invoice for Ride #{self.ride.id}"
