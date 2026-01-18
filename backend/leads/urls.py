from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeadViewSet, ContactViewSet

router = DefaultRouter()
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'contacts', ContactViewSet, basename='contact')

urlpatterns = [
    path('', include(router.urls)),
]
