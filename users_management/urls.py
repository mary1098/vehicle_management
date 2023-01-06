from django.urls import path as url
from users_management.views import *

urlpatterns = [
    url('api/super_admin', SuperAdminApi.as_view()),
    url('api/admin_new', AdminApi.as_view()),
    url('api/users', UserApi.as_view()),
]