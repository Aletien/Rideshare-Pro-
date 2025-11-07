from rest_framework import serializers
from rides.models import Ride, RideLocation, Rating

class RideLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideLocation
        fields = ['id', 'latitude', 'longitude', 'timestamp']

class RideSerializer(serializers.ModelSerializer):
    locations = RideLocationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Ride
        fields = [
            'id', 'passenger', 'driver', 'vehicle', 'pickup_location', 
            'dropoff_location', 'status', 'estimated_distance', 'estimated_duration',
            'estimated_fare', 'actual_fare', 'scheduled_time', 'started_at',
            'completed_at', 'cancelled_at', 'cancellation_reason', 'locations',
            'created_at', 'updated_at'
        ]

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'ride', 'rater', 'ratee', 'rating', 'comment', 'created_at']
