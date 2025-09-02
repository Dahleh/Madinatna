from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Cluster, Facility
from .serializers import CategorySerializer, ClusterSerializer, FacilitySerializer, FacilityWriteSerializer
from .permissions import IsOwnerOrAdminReadOnly, IsAdminOrManager


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ClusterViewSet(viewsets.ModelViewSet):
    queryset = Cluster.objects.all().order_by('name')
    serializer_class = ClusterSerializer
    permission_classes = [permissions.IsAuthenticated]


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.select_related('category', 'cluster', 'owner').prefetch_related('images').all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'address']

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAdminOrManager()]
        if self.action in ['update', 'partial_update']:
            return [IsOwnerOrAdminReadOnly()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FacilityWriteSerializer
        return FacilitySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.query_params.get('category')
        cluster_id = self.request.query_params.get('cluster')
        if category_id:
            qs = qs.filter(category_id=category_id)
        if cluster_id:
            qs = qs.filter(cluster_id=cluster_id)
        return qs

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        facilities = self.get_queryset().filter(owner=request.user)
        data = FacilitySerializer(facilities, many=True, context={'request': request}).data
        return Response(data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        facility = self.get_object()
        request.user.favorite_facilities.add(facility)
        return Response({"status": "favorited"})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unfavorite(self, request, pk=None):
        facility = self.get_object()
        request.user.favorite_facilities.remove(facility)
        return Response({"status": "unfavorited"})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def favorites(self, request):
        facilities = request.user.favorite_facilities.all()
        data = FacilitySerializer(facilities, many=True, context={'request': request}).data
        return Response(data)
