from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

class SignUpSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    # first_name=serializers.CharField()
    # last_name=serializers.CharField()
    class Meta:
        model=User
        fields=("email","password","first_name","last_name")
      
    def validate(self,attrs):
        print(attrs)
        if User.objects.filter(username=attrs['email']).exists():
             raise serializers.ValidationError({"message":"email already exists","status":"error"})
        return attrs
    def create(self,validated_data):
        
        
        user=User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class SignInSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model=User
        fields=("email","password")
      
    def validate(self,attrs):
        print(attrs)
        username=attrs['email']
        password=attrs['password']
        
        if username and password:
            user=authenticate(username=username,password=password)
            print(user)
            if user is None:
                raise serializers.ValidationError({"message": "Invalid credentials", "status": "error"})
        else:
            raise serializers.ValidationError({"message": "Must include email and password", "status": "error"})
        attrs['user'] = user
        return attrs
    
class UsersSerializer(serializers.ModelSerializer):
    
    name=serializers.SerializerMethodField()
    
    class Meta:
        model=User
        fields=("name","email")
    
    def get_name(self,obj):
        return obj.get_full_name()