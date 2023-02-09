import os
import re

from .conftest import root_dir


class TestWorkflow:

    def test_workflow(self):
        titles_workflow_basename = 'titles_workflow'

        yaml = f'{titles_workflow_basename}.yaml'
        is_yaml = yaml in os.listdir(root_dir)

        yml = f'{titles_workflow_basename}.yml'
        is_yml = yml in os.listdir(root_dir)

        if not is_yaml and not is_yml:
            assert False, (
                f'В каталоге {root_dir} не найден файл с описанием workflow '
                f'{yaml} или {yml}.\n'
                '(Это нужно для проверки тестами на платформе)'
            )

        if is_yaml and is_yml:
            assert False, (
                f'В каталоге {root_dir} не должно быть двух файлов {titles_workflow_basename} '
                'с расширениями .yaml и .yml\n'
                'Удалите один из них'
            )

        filename = yaml if is_yaml else yml

        try:
            with open(f'{os.path.join(root_dir, filename)}', 'r') as f:
                titles = f.read()
        except FileNotFoundError:
            assert False, f'Проверьте, что добавили файл {filename} в каталог {root_dir} для проверки'

        assert (
                re.search(r'on:\s*push:\s*branches:\s*-\smaster', titles) or
                'on: [push]' in titles or
                'on: push' in titles
        ), f'Проверьте, что добавили действие при пуше в файл {filename}'
        assert 'pytest' in titles, f'Проверьте, что добавили pytest в файл {filename}'
        assert 'appleboy/ssh-action' in titles, f'Проверьте, что добавили деплой в файл {filename}'
        assert 'appleboy/telegram-action' in titles, (
            'Проверьте, что настроили отправку telegram сообщения '
            f'в файл {filename}'
        )
