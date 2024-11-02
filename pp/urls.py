# pp/urls.py
from django.urls import path
from my_pp.views import HomeView, analyze_infringement, check_data,login_data,index_two

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('analyze/', analyze_infringement, name='analyze'),
    path('check_data/', check_data, name='check_data'),
    path('login_data/', login_data,name='login_data'),
    path('index_two/', index_two, name='index_two'),
]