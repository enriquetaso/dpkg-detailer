import pytest
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_package_list(client, package, dependency):
    response = client.get("/packages/")
    assert response.status_code == 200
    assert response.data["count"] == 2


@pytest.mark.django_db
def test_package_details(client, package, dependency):
    response = client.get(f"/packages/{package.name}/")
    assert response.status_code == 200
    assert response.data["name"] == "testpackage"
    assert response.data["dependencies"] == ["testdependency (https://test.com)"]
    assert response.data["reverse_dependencies"] == []


@pytest.mark.django_db
def test_package_delete_fails(client, package, dependency):
    response = client.delete(f"/packages/{package.name}/")
    assert response.status_code == 405
