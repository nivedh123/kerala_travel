from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('spots/',views.ListofSpot,name='list'),
    path('spotsuser/',views.ListofSpotuser,name='listuser'),
    path('spots/<int:pk>',views.DetailofSpot,name='detail'),
    path('add/',views.cretingView,name='create'),
    path('<int:pk>/edit/',views.updateTemp,name='edit'),
    path('login/',views.LoginTemp.as_view(),name='login'),
    path('logout',views.LogoutView.as_view(template_name='home/logout.html'),name='logout'),
    path('signup',views.register.as_view(),name='signup'),
    path('<int:pk>/delete',views.DeleteTemp.as_view(),name='delete'),
    path('<str:value>/districtvise',views.districtView,name='district'),
    path('<str:value>/remarkvise',views.remarkView,name='remark'),
    path('reviewdelete/<int:pk>/<int:pk1>',views.deleteReview, name='rdelete'),
    path('creteprofile/',views.profileview.as_view(),name='profilecreate'),
    path('about/',views.Aboutview.as_view(),name='about'),
    path('<int:pk>/profileedit',views.profileeditview,name='profileedit'),
    path('profile/XXXtru=568289482432832494rrjdgnvgru85<int:pk>/hhjfngjvvf=jrtngnfnjxnxnjgfn/jgfncknjtx=nudnfbkbn',views.profileDisplay.as_view(),name='profile')
]