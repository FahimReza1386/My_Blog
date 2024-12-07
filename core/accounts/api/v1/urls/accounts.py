from django.urls import path
from .. import views

urlpatterns=[
    # Registration User
    path("registration/" , views.RegistrationApi.as_view() , name="RegistrationApi"),

    # Change Password
    path("change_password/" , views.CustomChangePasswordApi.as_view() , name="ChangePasswordApi"),
    
    # Activation User Api
    path('activation/confirm/<str:token>', views.AccountActivation.as_view() , name="AccountsActivation"),
    # Resent Activation
    path('activation/resent/', views.ResentAccountActivation.as_view() , name="AccountsActivationResent"),

    # Reset Password
    
    # Login and Logout with Token
    path('token/login/' , views.CustomObtainAuthToken.as_view() , name="Login-Token"),
    path('token/logout/' , views.CustomObtainDiscardAuthToken.as_view() , name="Logout-Token"),

    # Login and Refresh and Verified With Jwt
    path('jwt/login/' , views.CustomObtainTokenPairView.as_view() , name="Login-jwt"),
    path('jwt/refresh/' , views.CustomTokenRefreshView.as_view() , name="refresh-jwt"),
    path('jwt/verified/' , views.CustomTokenVerifyView.as_view() , name="verified-jwt"),
    

]
