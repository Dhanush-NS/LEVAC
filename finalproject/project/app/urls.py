from django.urls import path
from .views import  mainpage,signup,login_view,edit_view,java,python,c,cpp,js,pyvideo,logout,javavideo,cvideo,jsvideo,dsavideo,base

urlpatterns = [
    path('',mainpage ,name='mainpage'),
    path('base/',base ,name='base'),
    path('signup/',signup ,name='signup'),
    path('login/',login_view ,name='login'),
    path('edit/',edit_view ,name='edit'),
    path('java/',java,name='java'),
    path('python/',python,name='python'),
    path('c/',c,name='c'),
    path('cpp/',cpp,name='cpp'),
    path('js/',js,name='js'),
    path('pyvideo/',pyvideo,name='pyvideo'),
    path('javavideo/',javavideo,name='javavideo'),
    path('cvideo/',cvideo,name='cvideo'),
    path('jsvideo/',jsvideo,name='jsvideo'),
    path('dsavideo/',dsavideo,name='dsavideo'),
    path('logout/',logout,name='logout'),
   
]