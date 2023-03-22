from django.urls import path, include
from users.views.users import UserRegistrationView


urlpatterns = [
    path('user/registration/', UserRegistrationView.as_view(), name='user-registration'),
]