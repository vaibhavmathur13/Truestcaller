from django.contrib import admin
from django.urls import path, include

from truestcaller import views as truestcaller_views

urlpatterns = [
    path('register/', truestcaller_views.RegisterUserAPIView.as_view(), name='register'),
    path('login/', truestcaller_views.LoginUserAPIView.as_view(), name='login'),
    path('mark-phone-number-spam/', truestcaller_views.PhoneNumberSpamMarkAPIView.as_view(),
         name='mark_phone_number_spam'),
    path('search-by-name/', truestcaller_views.SearchByNameAPIView.as_view(),
         name='search_by_name'),
    path('search-by-phone-number/', truestcaller_views.SearchByPhoneNumberAPIView.as_view(),
         name='search_by_phone_number'),
    path('logout/', truestcaller_views.LogoutAPIView.as_view(), name='logout'),
]
