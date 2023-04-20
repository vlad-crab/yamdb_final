import csv

from django.conf import settings
from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User

TABLES = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}
MANYTOMANY = {'genre_title.csv': {
    'title_id': Title,
    'genre_id': Genre,
    'order': ['title_id', 'genre_id']
}}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, csv_f in TABLES.items():
            model.objects.all().delete()
            with open(
                f'{settings.BASE_DIR}/static/data/{csv_f}',
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(
                    model(**data) for data in reader)
        for csv_f, links in MANYTOMANY:
            with open(
                f'{settings.BASE_DIR}/static/data/{csv_f}',
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    target = links[links['order'[0]]].objects.get(
                        id=row[links['order'[0]]]
                    )
                    sub = row[links['order'[1]]]
                    target.genre.add(sub)
        self.stdout.write(self.style.SUCCESS('Все данные загружены'))
