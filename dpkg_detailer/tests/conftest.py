import pytest
from django.contrib.auth.models import User
from dpkg_detailer.models import Package, Dependency


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="12345")


@pytest.fixture
def package(db):
    return Package.objects.create(
        name="testpackage",
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


@pytest.fixture
def dependency(db, package):
    dependency = Package.objects.create(
        name="testdependency",
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
        package=package, depends_on=dependency, dependency_type="Depends"
    )
    return dependency
