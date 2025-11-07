from rest_framework import serializers
from users.models import User, PassengerProfile, DriverProfile, Vehicle, AdminProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'user_type', 'is_verified', 'profile_picture']
        read_only_fields = ['id']

class PassengerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = PassengerProfile
        fields = ['id', 'user', 'home_address', 'work_address', 'favorite_locations', 'emergency_contact', 'rating', 'total_rides']

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'make', 'model', 'year', 'license_plate', 'color', 'seats', 'vehicle_type', 'registration_number', 'insurance_expiry', 'is_active']

class DriverProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    vehicles = VehicleSerializer(many=True, read_only=True)
    
    class Meta:
        model = DriverProfile
        fields = ['id', 'user', 'license_number', 'license_expiry', 'status', 'is_online', 'current_location', 'rating', 'total_rides', 'total_earnings', 'bank_account', 'vehicles']

class AdminProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = AdminProfile
        fields = ['id', 'user', 'department', 'permissions']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'phone_number', 'user_type']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
