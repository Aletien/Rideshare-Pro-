from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User, DriverProfile, PassengerProfile, Vehicle

class Ride(models.Model):
    STATUS_CHOICES = (
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    passenger = models.ForeignKey(PassengerProfile, on_delete=models.CASCADE, related_name='rides')
    driver = models.ForeignKey(DriverProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='rides')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    
    pickup_location = models.JSONField()  # {lat, lng, address}
    dropoff_location = models.JSONField()  # {lat, lng, address}
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    
    estimated_distance = models.FloatField(help_text="Distance in km")
    estimated_duration = models.IntegerField(help_text="Duration in minutes")
    estimated_fare = models.DecimalField(max_digits=10, decimal_places=2)
    actual_fare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    scheduled_time = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    cancellation_reason = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Ride #{self.id} - {self.status}"


class RideLocation(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='locations')
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"Location for Ride #{self.ride.id}"


class Rating(models.Model):
    ride = models.OneToOneField(Ride, on_delete=models.CASCADE, related_name='rating')
    
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    ratee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_received')
    
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('ride', 'rater')
    
    def __str__(self):
        return f"Rating: {self.rating}/5 for Ride #{self.ride.id}"
