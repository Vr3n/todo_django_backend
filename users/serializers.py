from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from users.models import Profile

from users.validators import password_regex_validator

from .utils import is_email_exists, is_mobile_exists

User = get_user_model()


class ReadOnlyModelSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        for field in fields:
            fields[field].read_only = True
        return fields


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(validators=[
                                     password_regex_validator],
                                     write_only=True,
                                     required=True,
                                     style={'input_type': 'password'}
                                     )

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return User
        raise serializers.ValidationError('Incorrect Credentials Provided!')


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[password_regex_validator],
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'mobile_number',
                  'username', 'password', 'password2']

    def validate_email(self, value):
        """
        Check for Email Exists Already
        """

        if is_email_exists(value):
            raise serializers.ValidationError('The Email already exists!')
        return value

    def validate_mobile_number(self, value):
        """
        Check for Mobile Number Exists Already
        """

        if is_mobile_exists(value):
            raise serializers.ValidationError(
                'The Mobile number already exists!')
        return value

    def validate(self, data):

        # Check if password2 matches password1.
        if data['password2'] > data['password']:
            raise serializers.ValidationError('Passwords Don\'t Match!')
        return data

    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        password = validated_data['password']
        email = validated_data['email']
        username = validated_data['username']
        mobile_number = validated_data['mobile_number']

        user = User(email=email, username=username,
                    mobile_number=mobile_number,
                    first_name=first_name,
                    last_name=last_name)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ReadOnlyProfileSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
