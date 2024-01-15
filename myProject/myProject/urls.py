from django.contrib import admin
from django.urls import path
from myProject.views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homePage,name='homePage'),
    path('signinPage/',signinPage,name='signinPage'),
    path('signupPage/',signupPage,name='signupPage'),
    path('logoutPage/',logoutPage,name='logoutPage'),
    path('dashboardPage/',dashboardPage,name='dashboardPage'),
    path('viewrentPage/',viewrentPage,name='viewrentPage'),
    path('add_rent_Page/',add_rent_Page,name='add_rent_Page'),
    path('deletePage/<str:myid>',deletePage,name='deletePage'),
    path('editPage/<str:myid>',editPage,name='editPage'),
    path('updatePage/',updatePage,name='updatePage'),
    path('applyPage/<str:myid>',applyPage,name='applyPage'),
    path('myaccount/',myaccount,name='myaccount'),
    path('EditProfilePage/',EditProfilePage,name='EditProfilePage'),
    path('changePasswordPage/',changePasswordPage,name='changePasswordPage'),
    path('createdrentByProfile/',createdrentByProfile,name='createdrentByProfile'),
    path('applied_rents/', applied_rents, name='applied_rents'),
    path('post_details/<int:post_id>/', post_details, name='post_details'),
    path('notifications_page/', notifications_page, name='notifications_page'),
    path('chat/',chatPage, name='chatPage'),
    path('profilepage/', profilepage, name='profilepage'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

