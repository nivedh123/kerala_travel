from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('spots/',views.ListofSpot,name='list'),
    path('spotsuser/',views.ListofSpotuser.as_view(),name='listuser'),
    path('spots/<int:pk>',views.DetailofSpot.as_view(),name='detail'),
    path('add/',views.cretingView,name='create'),
    path('<int:pk>/edit/',views.updateTemp,name='edit'),
    path('login/',views.LoginTemp.as_view(),name='login'),
    path('logout',views.LogoutView.as_view(template_name='home/logout.html'),name='logout'),
    path('signup',views.register,name='signup'),
    path('<int:pk>/delete',views.DeleteTemp.as_view(),name='delete'),
    path('<str:value>/districtvise',views.districtView,name='district')
]