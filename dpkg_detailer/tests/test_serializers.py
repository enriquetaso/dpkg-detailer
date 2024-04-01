import pytest
from dpkg_detailer.models import Package, Dependency
from dpkg_detailer.serializers import PackageSerializer


@pytest.mark.django_db
def test_package_serializer_dependency(package, dependency):
    reverse_dependency = Package.objects.create(
        name="testreverse",
        status="install ok installed",
        priority="optional",
        section="python",
        installed_size=1000,
        maintainer="Test Maintainer",
        architecture="all",
        version="1.0",
        description="Test Description",
        homepage="https://test.com",
        python_version="3.8",
    )
    Dependency.objects.create(
        package=reverse_dependency, depends_on=package, dependency_type="Depends"
    )
    package_data = PackageSerializer(package).data
    assert package_data["dependencies"] == ["testdependency (https://test.com)"]
    assert package_data["reverse_dependencies"] == ["testreverse (https://test.com)"]
    assert package_data["name"] == "testpackage"
    assert package_data["description"] == "Test Description"
