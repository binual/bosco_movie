from django.urls import path
from.import views
urlpatterns=[
    path("",views.home,name="home"),
    path('movie/<int:movie_id>/',views.movie_details, name='movie_details'), 
    path('user_register/',views.user_register, name='user_register'), 
    path('send_otp/', views.send_otp, name='send_otp'),  # Add this URL for sending OTP
    path('verify_otp/', views.verify_otp, name='verify_otp'),
   path('login_user/', views.login_user, name='login_user'),
   path('seat/<int:movie_id>/', views.seat, name='seat'),
   path('logout/', views.user_logout, name='user_logout'),
   path('theater_list/<int:movie_id>/', views.theater_list, name='theater_list'),

   path('ticket/', views.ticket, name='ticket'),
] 

