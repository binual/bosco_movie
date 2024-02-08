from django.urls import path
from.import views
urlpatterns=[
    
path('adminbosco_dash/',views.adminbosco_dash,name='adminbosco_dash'), 
path('add_theater/',views.add_theater,name='add_theater'),
path('theater_list/',views.theater_list,name='theater_list'),
path('ownerregister/', views.ownerregister, name='ownerregister'),

path('edit/<int:theater_id>/',views.edit_theater, name='edit_theater'),
path('delete/<int:theater_id>/',views.delete_theater, name='delete_theater'),
path('approve/',views.approve,name='approve'),

path('adminapproval/<int:pk>/',views.adminapproval, name='adminapproval'),
path('adminreject/<int:pk>/', views.adminreject, name='adminreject'),
path('welcome/',views.welcome, name='welcome'),

path('add_movie/',views.add_movie,name='add_movie'),
path('delete_movie/<int:movie_id>/',views.delete_movie, name='delete_movie'),

path('view_movies/',views.view_movies, name='view_movies'),
path('add_show/',views.add_show, name='add_show'),
path('show_list/', views.show_list, name='show_list'),
]