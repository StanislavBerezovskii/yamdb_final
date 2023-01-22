import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


class Command(BaseCommand):
    """Класс менеджмент команд."""

    # Словарь с названиями csv файлов и соответствующими им моделями.
    csvfiles_models = {
        'category.csv': Category,
        'genre.csv': Genre,
        'users.csv': User,
        'titles.csv': Title,
        'genre_title.csv': GenreTitle,
        'review.csv': Review,
        'comments.csv': Comment,
    }

    def get_data(self, csvfile):
        """Забирает данные из csv файла и возвращает список словарей."""
        file_path = os.path.join(settings.BASE_DIR, settings.DATA_PATH,
                                 csvfile)
        with open(file_path, 'r', encoding='UTF-8') as file:
            data = csv.DictReader(file)
            return list(data)

    def title_entries(self):
        """Добавляет записи в модель Title."""
        csv_file = 'titles.csv'
        model = self.csvfiles_models[csv_file]
        data = self.get_data(csv_file)
        for entry in data:
            id = entry['id']
            name = entry['name']
            year = entry['year']
            category = get_object_or_404(Category,
                                         pk=entry['category'])
            model.objects.get_or_create(
                id=id,
                name=name,
                year=year,
                category=category
            )
        total_objects = model.objects.count()
        self.terminal_message(csv_file, total_objects)

    def genretitle_entries(self):
        """Добавляет записи в модель GenreTitle."""
        csv_file = 'genre_title.csv'
        model = self.csvfiles_models[csv_file]
        data = self.get_data(csv_file)
        for entry in data:
            id = entry['id']
            title = get_object_or_404(Title, pk=entry['title_id'])
            genre = get_object_or_404(Genre, pk=entry['genre_id'])
            model.objects.get_or_create(
                id=id,
                title_id=title,
                genre_id=genre
            )
        total_objects = model.objects.count()
        self.terminal_message(csv_file, total_objects)

    def review_entries(self):
        """Добавляет записи в модель Review."""
        csv_file = 'review.csv'
        model = self.csvfiles_models[csv_file]
        data = self.get_data(csv_file)
        for entry in data:
            id = entry['id']
            title = get_object_or_404(Title, pk=entry['title_id'])
            text = entry['text']
            author = get_object_or_404(User, pk=entry['author'])
            score = entry['score']
            pub_date = entry['pub_date']
            try:
                model.objects.get_or_create(
                    id=id,
                    title=title,
                    text=text,
                    author=author,
                    score=score,
                    pub_date=pub_date
                )
            except IntegrityError:
                continue
        total_objects = model.objects.count()
        self.terminal_message(csv_file, total_objects)

    def comments_entries(self):
        """Добавляет записи в модель Comment."""
        csv_file = 'comments.csv'
        model = self.csvfiles_models[csv_file]
        data = self.get_data(csv_file)
        for entry in data:
            id = entry['id']
            review = get_object_or_404(Review, pk=entry['review_id'])
            text = entry['text']
            author = get_object_or_404(User, pk=entry['author'])
            pub_date = entry['pub_date']
            try:
                model.objects.get_or_create(
                    id=id,
                    review=review,
                    text=text,
                    author=author,
                    pub_date=pub_date,
                )
            except IntegrityError:
                continue
        total_objects = model.objects.count()
        self.terminal_message(csv_file, total_objects)

    def terminal_message(self, csvfile, total_objects):
        """Выводит в терминал информационное сообщение."""
        self.stdout.write(f'В модели файла {csvfile} записей: '
                          f'{total_objects}.')

    def handle(self, *args, **options):
        """Заполняет модели БД записями из csv файлов."""
        for csvfile, model in self.csvfiles_models.items():
            # Обращение к несложным моделям.
            if model in [Category, Genre, User]:
                data = self.get_data(csvfile)
                for entry in data:
                    model.objects.get_or_create(**entry)
                total_objects = model.objects.count()
                self.terminal_message(csvfile, total_objects)

        # Обращение к методам переноса данных в сложные модели.
        self.title_entries()
        self.genretitle_entries()
        self.review_entries()
        self.comments_entries()

        # Заключительное сообщение об успешном переносе данных.
        self.stdout.write('Все данные успешно перенесены.')
