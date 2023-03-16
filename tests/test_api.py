import pytest
import requests
import json

from django.contrib.auth.models import User
from rest_framework.test import APIClient


# @pytest.mark.django_db
# def test_jwt():
#     response = requests.post("http://localhost:8000/auth/jwt/create/", {"username": "admin", "password": "AutosaloonBOSS"})
#     token = json.loads(response.content)['access']
#     headers = {'Authorization': f'Bearer {token}',
#                'Content-Type': 'application/json'}
#     profile = requests.get("http://localhost:8000/trading/my_profile/", headers=headers)
#     print(profile.content)
#     assert response.status_code == 200


@pytest.mark.django_db(True)
def test_jwt(client):
    #user = User.objects.get(username='admin')
   # client.force_authenticate(user=user)
    response = client.get('http://localhost:8000/cars/autos/')
    print(response.json())
    assert response.status_code == 200
