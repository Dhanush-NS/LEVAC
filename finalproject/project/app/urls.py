from django.urls import path
from .views import  (mainpage,base,signup,login_view,edit_view,logout,java,python,c,dsa,
cpp,js,pyvideo,javavideo,cvideo,jsvideo,dsavideo,cppvideo, leetcode)
urlpatterns = [
    path('',mainpage ,name='mainpage'),
    path('base/',base ,name='base'),

    # Registration urls
    path('signup/',signup ,name='signup'),
    path('login/',login_view ,name='login'),
    path('edit/',edit_view ,name='edit'),
    path('logout/',logout,name='logout'),


    # tutor urls
    path('java/',java,name='java'),
    path('python/',python,name='python'),
    path('c/',c,name='c'),
    path('cpp/',cpp,name='cpp'),
    path('js/',js,name='js'),
    path('dsa/',dsa,name='dsa'),
    path('leetcode/',leetcode,name='leetcode'),


    #video urls
    path('pyvideo/',pyvideo,name='pyvideo'),
    path('javavideo/',javavideo,name='javavideo'),
    path('cvideo/',cvideo,name='cvideo'),
    path('jsvideo/',jsvideo,name='jsvideo'),
    path('dsavideo/',dsavideo,name='dsavideo'),
    path('cppvideo/',cppvideo,name='cppvideo'),
   
]