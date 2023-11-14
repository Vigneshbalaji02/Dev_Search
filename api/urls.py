from django.urls import path
from .import views


from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns =[
    path('', views.getroutes),
    path('Projects', views.getproject),
    path('Projects/<str:pk>', views.getprojects),

    

    path('users/token',TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('users/token/refresh',TokenRefreshView.as_view(), name="token_refresh"),

]