from django.db import models


class Package(models.Model):
    name = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    priority = models.CharField(max_length=100, blank=True, null=True)
    section = models.CharField(max_length=100, blank=True, null=True)
    installed_size = models.IntegerField(default=0)
    maintainer = models.CharField(max_length=255, blank=True, null=True)
    architecture = models.CharField(max_length=100, blank=True, null=True)
    version = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    homepage = models.URLField(blank=True, null=True)
    python_version = models.CharField(max_length=100, blank=True, null=True)
    dependencies = models.ManyToManyField(
        "self", through="Dependency", symmetrical=False, null=True, blank=True
    )
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Dependency(models.Model):
    DEPENDENCY_CHOICES = [
        ("Depends", "Depends"),
        ("Suggests", "Suggests"),
        ("Conflicts", "Conflicts"),
    ]
    package = models.ForeignKey(
        Package, related_name="from_dependencies", on_delete=models.CASCADE
    )
    depends_on = models.ForeignKey(
        Package, related_name="to_dependencies", on_delete=models.CASCADE
    )
    dependency_type = models.CharField(
        max_length=50, choices=DEPENDENCY_CHOICES, default="Depends"
    )

    def __str__(self):
        return f"{self.from_package.name} depends on {self.depends_on}"
