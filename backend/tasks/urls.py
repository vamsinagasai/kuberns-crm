from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, VisitViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'visits', VisitViewSet, basename='visit')

urlpatterns = [
    path('', include(router.urls)),
]
