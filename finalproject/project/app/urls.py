from django.urls import path
from .views import  mainpage,signup,login,java,python,c,cpp,js,pyvideo,logout

urlpatterns = [
    path('',mainpage ,name='mainpage'),
    path('signup/',signup ,name='signup'),
    path('login/',login ,name='login'),
    path('java/',java,name='java'),
    path('python/',python,name='python'),
    path('c/',c,name='c'),
    path('cpp/',cpp,name='cpp'),
    path('js/',js,name='js'),
    path('pyvideo/',pyvideo,name='pyvideo'),
    path('logout/',logout,name='logout'),
   
]