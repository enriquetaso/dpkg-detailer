from rest_framework import viewsets
from .models import Package
from .serializers import PackageSerializer


class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Package.objects.all().prefetch_related(
        "from_dependencies", "to_dependencies"
    )
    serializer_class = PackageSerializer
    lookup_field = "name"
