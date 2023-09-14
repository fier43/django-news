from django.core.management.base import BaseCommand, CommandError
from simpleapp.models import News, Category


class Command(BaseCommand):
    help = "удаляет все новости одной категории"  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнится при вызове вашей команды
        self.stdout.readable()
        self.stdout.write("какую категорию вы хотите удалить? напишите от 1 до 3")
        pk = input()
        news = News.objects.filter(category=pk)
        self.stdout.write(
            "вы точно хотите удалить все новости данной категории? yes/no"
        )  # спрашиваем пользователя, действительно ли он хочет удалитьь категорию
        answer = input()  # считываем подтверждение

        if answer == "yes":  # в случае подтверждения действительно удаляем категорию
            news.delete()
            self.stdout.write(self.style.SUCCESS("Succesfully wiped products!"))
            return

        self.stdout.write(
            self.style.ERROR("Access denied")
        )  # в случае неправильного подтверждения, говорим, что в доступе отказано
