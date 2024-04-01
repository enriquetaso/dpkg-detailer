import re
import os
from django.core.management.base import BaseCommand, CommandError
from dpkg_detailer.models import Package, Dependency
from django.db import transaction


class Command(BaseCommand):
    help = "Imports package information from /var/lib/dpkg/status or a specified file"

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            nargs="?",
            default="/var/lib/dpkg/status",
            help="Optional file path to import packages from",
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]
        if not os.path.exists(file_path):
            raise CommandError(f'File "{file_path}" does not exist.')
        self.stdout.write(
            self.style.SUCCESS(f"Starting import of packages from {file_path}")
        )
        self.import_packages_and_dependencies(file_path)
        self.stdout.write(self.style.SUCCESS("Import completed"))

    def import_packages_and_dependencies(self, file_path):
        with open(file_path, "r") as f:
            package_data = f.read()
        total_package, total_dependency = self.parse_packages(package_data)
        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {total_package} packages. Created {total_dependency} dependencies."
            )
        )

    def parse_packages(self, package_data):
        count_package = 0
        count_dependency = 0
        packages_raw = package_data.strip().split("\n\n")
        for package_str in packages_raw:
            fields, dependency_fields = self.parse_package_fields(package_str)
            with transaction.atomic():
                package, created = Package.objects.update_or_create(
                    name=fields["name"], defaults=fields
                )
                if created:
                    count_package += 1

                if dependency_fields:
                    dependencies = self.parse_dependencies(dependency_fields, package)
                    count_dependency += len(dependencies)
        return count_package, count_dependency

    def parse_package_fields(self, package_str):
        field_pattern = re.compile(
            r"^(?P<name>[A-Za-z-]+): (?P<value>.+)$", re.MULTILINE
        )
        fields = dict(field_pattern.findall(package_str))

        multiline_fields = ["Description"]
        for field in multiline_fields:
            if field in fields:
                value_start = package_str.index(f"{field}: ") + len(f"{field}: ")
                value_end = (
                    package_str.index("\n\n", value_start)
                    if "\n\n" in package_str[value_start:]
                    else len(package_str)
                )
                fields[field] = (
                    package_str[value_start:value_end].replace("\n ", "\n").strip()
                )

        package_data = {
            "name": fields.get("Package"),
            "status": fields.get("Status"),
            "priority": fields.get("Priority"),
            "section": fields.get("Section"),
            "installed_size": int(fields.get("Installed-Size", 0)),
            "maintainer": fields.get("Maintainer"),
            "architecture": fields.get("Architecture"),
            "version": fields.get("Version"),
            "description": fields.get("Description"),
            "homepage": fields.get("Homepage"),
            "python_version": fields.get("Python-Version"),
        }

        dependency_data = fields.get("Depends")
        return package_data, dependency_data

    def parse_dependencies(self, dependency_str, parent_package):
        dependencies = []
        if dependency_str:
            for dep in dependency_str.split(","):
                alternatives = dep.split(" | ")
                for alt in alternatives:
                    dependency_name = alt.strip().split(" ")[0]
                    dependency_package, _ = Package.objects.update_or_create(
                        name=dependency_name
                    )
                    _, created = Dependency.objects.update_or_create(
                        package=parent_package,
                        depends_on=dependency_package,
                        dependency_type="Depends",
                    )
                    if created:
                        dependencies.append(dependency_package)
        return dependencies
