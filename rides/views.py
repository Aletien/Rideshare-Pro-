from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rides.models import Ride, RideLocation, Rating
from rides.serializers import RideSerializer, RideLocationSerializer, RatingSerializer
from users.models import PassengerProfile, DriverProfile

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'passenger_profile'):
            return Ride.objects.filter(passenger__user=user)
        elif hasattr(user, 'driver_profile'):
            return Ride.objects.filter(driver__user=user)
        return Ride.objects.none()
    
    @action(detail=False, methods=['post'])
    def request_ride(self, request):
        try:
            passenger = PassengerProfile.objects.get(user=request.user)
        except PassengerProfile.DoesNotExist:
            return Response({'error': 'Passenger profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RideSerializer(data=request.data)
        if serializer.is_valid():
            ride = serializer.save(passenger=passenger, status='requested')
            return Response(RideSerializer(ride).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def accept_ride(self, request, pk=None):
        ride = self.get_object()
        try:
            driver = DriverProfile.objects.get(user=request.user)
        except DriverProfile.DoesNotExist:
            return Response({'error': 'Driver profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if ride.status != 'requested':
            return Response({'error': 'Ride is not available'}, status=status.HTTP_400_BAD_REQUEST)
        
        ride.driver = driver
        ride.status = 'accepted'
        ride.save()
        return Response(RideSerializer(ride).data)
    
    @action(detail=True, methods=['post'])
    def start_ride(self, request, pk=None):
        ride = self.get_object()
        if ride.status != 'accepted':
            return Response({'error': 'Ride cannot be started'}, status=status.HTTP_400_BAD_REQUEST)
        
        ride.status = 'started'
        ride.started_at = timezone.now()
        ride.save()
        return Response(RideSerializer(ride).data)
    
    @action(detail=True, methods=['post'])
    def complete_ride(self, request, pk=None):
        ride = self.get_object()
        if ride.status != 'started':
            return Response({'error': 'Ride cannot be completed'}, status=status.HTTP_400_BAD_REQUEST)
        
        ride.status = 'completed'
        ride.completed_at = timezone.now()
        ride.actual_fare = request.data.get('actual_fare', ride.estimated_fare)
        ride.save()
        return Response(RideSerializer(ride).data)
    
    @action(detail=True, methods=['post'])
    def cancel_ride(self, request, pk=None):
        ride = self.get_object()
        if ride.status in ['completed', 'cancelled']:
            return Response({'error': 'Ride cannot be cancelled'}, status=status.HTTP_400_BAD_REQUEST)
        
        ride.status = 'cancelled'
        ride.cancelled_at = timezone.now()
        ride.cancellation_reason = request.data.get('reason', '')
        ride.save()
        return Response(RideSerializer(ride).data)

class RideLocationViewSet(viewsets.ModelViewSet):
    queryset = RideLocation.objects.all()
    serializer_class = RideLocationSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def update_location(self, request):
        ride_id = request.data.get('ride_id')
        try:
            ride = Ride.objects.get(id=ride_id)
        except Ride.DoesNotExist:
            return Response({'error': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)
        
        location = RideLocation.objects.create(
            ride=ride,
            latitude=request.data.get('latitude'),
            longitude=request.data.get('longitude')
        )
        return Response(RideLocationSerializer(location).data, status=status.HTTP_201_CREATED)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def rate_ride(self, request):
        ride_id = request.data.get('ride_id')
        try:
            ride = Ride.objects.get(id=ride_id)
        except Ride.DoesNotExist:
            return Response({'error': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)
        
        rating = Rating.objects.create(
            ride=ride,
            rater=request.user,
            ratee=ride.driver.user if ride.driver else ride.passenger.user,
            rating=request.data.get('rating'),
            comment=request.data.get('comment', '')
        )
        return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED)
