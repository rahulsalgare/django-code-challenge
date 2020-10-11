from rest_framework import serializers
# from core.models import Account
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from .models import MyUser
from django.core.mail import send_mail
from django.template.loader import render_to_string
from phonenumber_field.serializerfields import PhoneNumberField

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    phone = PhoneNumberField( validators=[UniqueValidator(queryset=MyUser.objects.all(),message="Account with this phone number already exists")])

    class Meta:
        model = MyUser
        fields = ['first_name','last_name','email','phone','date_of_birth','password','password2']


    def save(self):
        if self.instance is not None:
            self.instance = self.update(self.instance, self.validated_data)
        else:
            password = self.validated_data['password']
            password2 = self.validated_data['password2']

            if password != password2:
                raise serializers.ValidationError({"password":"Passwords must match"})
            else:
                us = MyUser(first_name=self.validated_data['first_name'],
                            last_name=self.validated_data['last_name'],
                            email=self.validated_data['email'],
                            phone=self.validated_data['phone'],
                            date_of_birth=self.validated_data['date_of_birth'],
                            )
                us.set_password(password)
                us.save()
                # htmlmessage = render_to_string('core/welcometemplate.html')
                # send_mail(
                #             'Subject here',
                #              '',
                #             'rsalgare95@gmail.com',
                #             [us.email],
                #             html_message=htmlmessage,
                #             fail_silently=False,
                #         )
                return us

class UpdateSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField( validators=[UniqueValidator(queryset=MyUser.objects.all(),message="Account with this phone number already exists")],required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(validators=[UniqueValidator(queryset=MyUser.objects.all(),message="Account with this email already exists")],required=False)

    class Meta:
        model= MyUser
        fields = ['first_name','last_name','phone','email']
