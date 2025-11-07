from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from users.models import User, PassengerProfile, DriverProfile
from users.serializers import (
    UserSerializer, UserRegistrationSerializer, 
    PassengerProfileSerializer, DriverProfileSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Create profile based on user type
            if user.user_type == 'passenger':
                PassengerProfile.objects.create(user=user)
            elif user.user_type == 'driver':
                DriverProfile.objects.create(user=user)
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class PassengerProfileViewSet(viewsets.ModelViewSet):
    queryset = PassengerProfile.objects.all()
    serializer_class = PassengerProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PassengerProfile.objects.filter(user=self.request.user)

class DriverProfileViewSet(viewsets.ModelViewSet):
    queryset = DriverProfile.objects.all()
    serializer_class = DriverProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DriverProfile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def go_online(self, request):
        try:
            driver = DriverProfile.objects.get(user=request.user)
            driver.is_online = True
            driver.save()
            return Response({'status': 'Driver is now online'})
        except DriverProfile.DoesNotExist:
            return Response({'error': 'Driver profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def go_offline(self, request):
        try:
            driver = DriverProfile.objects.get(user=request.user)
            driver.is_online = False
            driver.save()
            return Response({'status': 'Driver is now offline'})
        except DriverProfile.DoesNotExist:
            return Response({'error': 'Driver profile not found'}, status=status.HTTP_404_NOT_FOUND)
