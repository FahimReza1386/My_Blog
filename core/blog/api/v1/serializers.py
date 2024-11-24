from rest_framework import serializers # type: ignore
from django.contrib.auth.password_validation import validate_password
from accounts.models import User
from django.core import exceptions
