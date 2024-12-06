from django.urls import path
from .. import views

urlpatterns=[
    # Registration User
    path("registration/" , views.RegistrationApi.as_view() , name="RegistrationApi"),

    # Change Password
    path("change_password/" , views.CustomChangePasswordApi.as_view() , name="ChangePasswordApi"),
    # Activation User Api
    
    # Resent Activation
    # Reset Password
    # Login Token
    # 


]
