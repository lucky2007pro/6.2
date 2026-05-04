from rest_framework import serializers
from .models import User
from rest_framework.exceptions import ValidationError

class SignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    year = serializers.IntegerField(required=True)
    class Meta:
        model = User
        # include confirm_password so it can be validated but not returned
        fields = ['username', 'password', 'confirm_password', 'email', 'year']

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError('Parollar mos emas!')

        if len(password) < 8:
            raise ValidationError('Parol 8 tadan ortiq belgilardan iborat bo\'lishi kerak!')

        return data

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError('Bu username allaqachon ro\'yxatdan o\'tgan!')
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError('Bu email allaqachon ro\'yxatdan o\'tgan!')
        return email

    def create(self, validated_data):
        # Pop confirm_password because it's not a model field
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

