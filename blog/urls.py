from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/blog',views.Detailofblog,name='blog'),
    path('reviewdeleteblog/<int:pk>/<int:pk1>',views.deleteReview, name='rdeleteblog'),
    path('createblog/',views.creatingView,name='createblog'),
    path('<int:pk>/editblog/',views.updateTemp,name='editblog'),
    path('bloglist',views.ListofBlog,name='listblog'),
    path('<int:pk>/rblog',views.DeleteTemp.as_view(),name='deleteblog')
]