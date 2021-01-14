"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include, reverse_lazy
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from users.views import ObtainAuthToken, CreateUserViewSet, MeView
from orders.views import OrderViewSet, PaymentViewSet

router = DefaultRouter()
router.register("orders", OrderViewSet)
router.register("payment", PaymentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api-token-auth/", ObtainAuthToken.as_view()),
    path("registration/", CreateUserViewSet.as_view()),
    path("me/", MeView.as_view({'get': 'retrieve'})),
    # path('api/order', OrderView.as_view(), name='make a order'),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

