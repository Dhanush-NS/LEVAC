from django.urls import path
from .views import  (mainpage,base,signup,login_view,edit_view,logout,java,python,c,dsa,
cpp,js,pyvideo,javavideo,cvideo,jsvideo,dsavideo,cppvideo, hackerrank,editor, save_code, run_code,chat,chat_with_gemini,contact_view,check_email,check_username)
urlpatterns = [
    path('',mainpage ,name='mainpage'),
    path('base/',base ,name='base'),
    
    path('editor/', editor, name='editor'),
    path("save-code/", save_code, name="save_code"),
    path("run_code/", run_code, name="run_code"),
    path('chat/',chat,name='chat'),
    path('contact/', contact_view, name='contact'),
    path('check_username/', check_username, name='check_username'),
    path('check_email/', check_email, name='check_email'),
    path('chat/api/', chat_with_gemini, name='chat_with_gemini'),
    # Registration urls
    path('signup/',signup ,name='signup'),
    path('login/',login_view ,name='login'),
    path('edit/',edit_view ,name='edit'),
    path('logout/',logout,name='logout'),
    # path('profile/', profile_view, name='profile'),


    # tutor urls
    path('java/',java,name='java'),
    path('python/',python,name='python'),
    path('c/',c,name='c'),
    path('cpp/',cpp,name='cpp'),
    path('js/',js,name='js'),
    path('dsa/',dsa,name='dsa'),
    path('hackerrank/',hackerrank,name='hackerrank'),


    #video urls
    path('pyvideo/',pyvideo,name='pyvideo'),
    path('javavideo/',javavideo,name='javavideo'),
    path('cvideo/',cvideo,name='cvideo'),
    path('jsvideo/',jsvideo,name='jsvideo'),
    path('dsavideo/',dsavideo,name='dsavideo'),
    path('cppvideo/',cppvideo,name='cppvideo'),
   
  
    
]