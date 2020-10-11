import json
from django.test import TestCase
from .models import MyUser
from django.core.exceptions import ValidationError
from django.db import IntegrityError
# from django.db.backends.sqlite3.base import IntegrityError
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import  Token
# Create your tests here.

client = Client()

class UserValidation(TestCase):
    def setup(self):
        MyUser.objects.create(first_name="test2", last_name="test2",
                      phone="+919325270455", email="test3@gmail.com",
                      date_of_birth='2015-10-8', password="test")

    def test_phone_validation(self):
        data1 = dict(first_name="test2", last_name="test2",
                      phone="+919325270482", email="test2@gmail.com",
                      date_of_birth='2015-10-8', password="test")

        data2 = dict(first_name="test", last_name="test",
                               phone="+919325270482", email="test2@gmail.com",
                               date_of_birth='2015-10-8', password="test")

        self.user1 = MyUser.objects.create(**data1)
        user2 = MyUser(**data2)
        self.assertRaises(IntegrityError, user2.save)



class CreateUser(TestCase):
    valid_payload={}
    invalid_payload={}

    def setup(self):
        self.valid_payload = {

            "first_name":"new",
            "last_name":"new",
            "email":"new@gmail.com",
            "date_of_birth":"1995-01-25",
            "phone":"+918668972155",
            "password":"test",
            "password2":"test"
        }

        self.invalid_payload = {

            "first_name":"test",
            "last_name":"test",
            "email":"test@gmail.com",
            "date_of_birth":"1995-023-25",
            "phone":"+9186645d72199",
            "password":"test",
            "password2":"test "
        }

    def test_create_user(self):
        response = client.post(
            reverse('core:register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invalid_user(self):
        response = client.post(
            reverse('core:register'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateUser(TestCase):
    valid_payload={}
    def setup(self):

        self.valid_payload = {
            "first_name":"update test"
        }

    def test_update_unauthorised_user(self):
        user = MyUser.objects.create(first_name="test2", last_name="test2",
                      phone="+919325270455", email="test3@gmail.com",
                      date_of_birth='2015-10-8', password="test")
        tkn = Token.objects.get(user=user)

            response = client.put(
            reverse('core:update', kwargs={'pk': user.id}, **header),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class DeletetUser(TestCase):
    def test_delete_unauthorized_user(self):
        user = MyUser.objects.create(first_name="test2", last_name="test2",
                      phone="+919325270455", email="test3@gmail.com",
                      date_of_birth='2015-10-8', password="test")
        response = client.delete(
            reverse('core:delete', kwargs={'pk': user.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
