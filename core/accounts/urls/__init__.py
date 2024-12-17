from django.urls import path, include

urlpatterns = [
    path("", include("accounts.urls.accounts")),
    # path("profile/" , include("accounts.urls.profile")),
]
