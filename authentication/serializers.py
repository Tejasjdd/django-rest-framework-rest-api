from . models import User
from rest_framework import serializers
from phonenumber_field.modelfields import PhoneNumberField

class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    email = serializers.EmailField(max_length=80)
    phone_number = PhoneNumberField(null=False,blank=False)
    password = serializers.CharField(min_length=8,write_only=True)

    class Meta:
        model = User
        fields = ['username','email','phone_number','password']

    def create(self,validated_data):
        user=User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number']
        )
        
        user.set_password(validated_data['password'])
        user.save()
        return user