from django.urls import path,re_path,include
#django自带的登录装饰器
from apps.user.views import  LogoutView,RegisterView,ActiveView,LoginView,UserInfoView,UserOrderView,AddressView
# from django.contrib.auth.decorators import login_required
urlpatterns = [
    re_path(r'^register$',RegisterView.as_view(),name='register'), #注册
    re_path(r'^active/(?P<token>.*)$',ActiveView.as_view(),name='active'),#激活
    re_path(r'^login$',LoginView.as_view(),name='login'), #登录
    re_path(r'^logout$',LogoutView.as_view(),name='logout'), #退出

    # re_path(r'^order$',login_required(UserOrderView.as_view()),name='order'),
    # re_path(r'^address$',login_required(AddressView.as_view()),name='address'),
    # re_path(r'^$',login_required(UserInfoView.as_view()),name='user'), #用户中心信息页

    re_path(r'^order$',UserOrderView.as_view(),name='order'),
    re_path(r'^address$',AddressView.as_view(),name='address'),
    re_path(r'^$',UserInfoView.as_view(),name='user'),
]
