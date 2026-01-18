from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, LoginSerializer
from .permissions import IsManagerOrAdmin, IsAdminOrSelf


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User management.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user() or user.is_sales_manager():
            return User.objects.all()
        # Sales executives can only see themselves
        return User.objects.filter(id=user.id)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminOrSelf()]
        return super().get_permissions()
    
    @action(detail=False, methods=['post'], permission_classes=[])
    def login(self, request):
        """User login endpoint."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user information."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
