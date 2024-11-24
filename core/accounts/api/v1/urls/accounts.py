from django.urls import path
from .. import views

urlpatterns=[
    # Registration User
    path("registration/" , views.RegistrationApi.as_view() , name="RegistrationApi"),

    # Change Password
    # path("change_password/" , views.ChangePasswordApi.as_view() , name="ChangePassword"),

    # Activation User Api
    
    # Resent Activation
    # Reset Password
    # Login Token
    # 


]
