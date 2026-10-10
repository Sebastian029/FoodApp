from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from api.models import Recipe
from api.utils import upload_recipes_from_csv


class Command(BaseCommand):
    help = "Load recipes and their ingredients from a semicolon-separated CSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            "path",
            nargs="?",
            default=str(Path(settings.BASE_DIR) / "updated_data.csv"),
            help="CSV file to load (default: backend/updated_data.csv).",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Load even if recipes already exist (this creates duplicates).",
        )

    def handle(self, *args, **options):
        existing = Recipe.objects.count()
        if existing and not options["force"]:
            raise CommandError(
                f"{existing} recipes already exist. Use --force to load anyway "
                "(this creates duplicates)."
            )

        success, message = upload_recipes_from_csv(options["path"])
        if not success:
            raise CommandError(message)
        self.stdout.write(
            self.style.SUCCESS(f"{message} Recipes in database: {Recipe.objects.count()}.")
        )
