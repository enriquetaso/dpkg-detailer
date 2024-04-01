from rest_framework import serializers
from .models import Package, Dependency


class PackageSerializer(serializers.ModelSerializer):
    dependencies = serializers.SerializerMethodField()
    reverse_dependencies = serializers.SerializerMethodField()

    class Meta:
        model = Package
        fields = ("name", "description", "dependencies", "reverse_dependencies")

    def get_dependencies(self, obj):
        dependencies = obj.from_dependencies.all()
        return [self.format_package(dep.depends_on) for dep in dependencies]

    def get_reverse_dependencies(self, obj):
        reverse_deps = obj.to_dependencies.all()
        return [self.format_package(dep.package) for dep in reverse_deps]

    def format_package(self, package):
        if package.homepage:
            return f"{package.name} ({package.homepage})"
        return package.name
