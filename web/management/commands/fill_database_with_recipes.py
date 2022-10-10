from contextlib import suppress
from decimal import Decimal
from urllib.parse import urljoin

import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from io import BytesIO
from bs4 import BeautifulSoup

from web.models import Ingredient, IngredientQuantity, Recipe


def get_last_page_of_category(category_url):
    response = requests.get(category_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    end_page = int(soup.select('.pagination a')[-2].text)
    return end_page


def download_image(image_url):
    response = requests.get(image_url)
    response.raise_for_status()
    file = NamedTemporaryFile()
    file.write(response.content)
    file.flush()
    return file


def parse_category_for_recipe_urls(category_url, max_pages_in_category):
    recipe_urls = []
    last_page_of_category = get_last_page_of_category(category_url)
    last_page_to_parse = min(last_page_of_category, max_pages_in_category)
    for page_number in range(1, last_page_to_parse+1):
        with suppress(requests.HTTPError):
            payload = {
                'page': page_number
            }
            response = requests.get(category_url, params=payload)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            recipes = soup.select('.title_recept')
            for recipe in recipes:
                link = recipe.select_one('a')['href']
                recipe_url = urljoin('https://вкуснофф.рф', link)
                recipe_urls.append(recipe_url)
    return recipe_urls


def parse_recipe_page(recipe_url):
    response = requests.get(recipe_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    name = soup.select_one('h1.title_h2').text
    nutrients_numbers = soup.select('.ei_count')
    calories = nutrients_numbers[0].text.strip()
    proteins = nutrients_numbers[1].text.strip()
    fats = nutrients_numbers[2].text.strip()
    carbs = nutrients_numbers[3].text.strip()
    nutrients = {
        'calories': round(Decimal(calories), 1),
        'proteins': round(Decimal(proteins), 1),
        'fats': round(Decimal(fats), 1),
        'carbs': round(Decimal(carbs), 1),
    }
    portions = int(soup.select_one('.inp_count_porcion').text)
    ingredients = []
    for ingredient in soup.select('.ingredients-list-wrapper .ing_item'):
        weight_per_portion = round(
            Decimal(ingredient['data-weight-in-gram']) / portions, 3
        )
        amount_per_portion = round(
            Decimal(ingredient['data-count']) / portions, 3
        )
        ingredients.append({
            'name': ingredient.select_one('.ing_item_name').text,
            'weight_per_portion': weight_per_portion,
            'amount_per_portion': amount_per_portion,
            'unit_label': ingredient['data-unit-label']
        })
    steps = []
    for step in soup.select('.step_text'):
        steps.append(step.text.strip())
    end_result = soup.select_one('p.recept_text').text.strip()
    cover_image_url = urljoin(
        'https://вкуснофф.рф',
        soup.select_one('.recept_photo_img')['src']
    )
    recipe = {
        'name': name,
        'nutrients': nutrients,
        'ingredients': ingredients,
        'steps': steps,
        'end_result': end_result,
        'cover_image': cover_image_url
    }
    return recipe


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--pages_for_category',
            nargs='?',
            const='1',
            default='1',
            help='Specify the number of pages to parse in each category',
        )

    def handle(self, *args, **options):
        menu_types_and_category_urls = {
            'Классическое': 'https://xn--b1aqjenlka.xn--p1ai/recepty/obed/',
            'Низкоуглеводное': 'https://xn--b1aqjenlka.xn--p1ai/recepty/nizkokalorijnoe/',
            'Вегетерианское': 'https://xn--b1aqjenlka.xn--p1ai/recepty/vegetarianskoe/',
            'Кето': 'https://xn--b1aqjenlka.xn--p1ai/recepty/keto/',
        }
        recipes_data = {}
        max_pages_in_category = int(options['pages_for_category'])
        for menu_type, category_url in menu_types_and_category_urls.items():
            recipe_urls = parse_category_for_recipe_urls(
                category_url,
                max_pages_in_category
            )
            menu_type_recipes = [parse_recipe_page(url) for url in recipe_urls]
            recipes_data[menu_type] = menu_type_recipes
        ingredients = set()
        for category in recipes_data.values():
            for recipe in category:
                for ingredient in recipe['ingredients']:
                    ingredients.add(ingredient['name'])
        ingredients = [Ingredient(name=ingredient) for ingredient in ingredients]
        Ingredient.objects.bulk_create(ingredients)
        ingredient_to_id = {}
        for ingredient in Ingredient.objects.all():
            ingredient_to_id[ingredient.name] = ingredient.id
        category_to_menu_type = {
            'Классическое': 'CL',
            'Низкоуглеводное': 'LC',
            'Вегетерианское': 'VG',
            'Кето': 'KT',
        }
        for category_name, category_recipes in recipes_data.items():
            for recipe in category_recipes:
                cover_image = download_image(recipe['cover_image'])
                created_recipe = Recipe.objects.create(
                    name=recipe['name'],
                    steps='\n'.join(recipe['steps']),
                    end_result=recipe['end_result'],
                    calories=recipe['nutrients']['calories'],
                    proteins=recipe['nutrients']['proteins'],
                    fats=recipe['nutrients']['fats'],
                    carbs=recipe['nutrients']['carbs'],
                    menu_type=category_to_menu_type[category_name],
                )
                created_recipe.cover_image.save(
                    f'{recipe["name"]}.jpg',
                    File(cover_image),
                    save=True
                )
                IngredientQuantity.objects.bulk_create([
                    IngredientQuantity(
                        ingredient_id=ingredient_to_id[ingredient['name']],
                        recipe_id=created_recipe.id,
                        weight_per_portion=ingredient['weight_per_portion'],
                        amount_per_portion=ingredient['amount_per_portion'],
                        unit_label=ingredient['unit_label']
                    ) for ingredient in recipe['ingredients']
                ])
