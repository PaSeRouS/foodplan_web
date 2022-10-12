import random
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegisterForm, UpdateUserDetailsForm
from .models import Allergy, SubscriptionType, Subscription, Recipe, SubscriptionRecipe


@login_required(login_url='/login/')
def order(request):
    if request.method == 'POST':
        user = request.user

        subs_type = SubscriptionType.objects.get(
            name__contains=request.POST['menu_type'],
            duration=request.POST['duration']
        )

        price = subs_type.duration * subs_type.price
        valid_until = datetime.today()+ relativedelta(
            months=int(request.POST['duration'])
        )

        subscription = Subscription.objects.create(
            user=user,
            number_of_meals=request.POST['number_of_meals'],
            number_of_person=request.POST['number_of_person'],
            subs_type=subs_type,
            price=price,
            valid_until=valid_until
        )

        for allergy in request.POST.getlist('allergies'):
            if allergy:
                subscription.allergies.add(
                    Allergy.objects.get(
                        name=allergy
                    )
                )

        subscription.save()
        return redirect('lk')

    else:
        context = {
            'allergies': [allergy.name for allergy in Allergy.objects.all()]
        }

        return render(request, 'order.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('lk')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            return redirect('start_page')
    else:
        form = RegisterForm()
    return render(request, 'registration.html', {'form': form})


@login_required(login_url='/login/')
def lk(request):
    if request.method == 'POST':
        form = UpdateUserDetailsForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('lk')
    else:
        form = UpdateUserDetailsForm(request.user)
    try:
        subscription = Subscription.objects.filter(user=request.user)[0]
        subscription_id = subscription.id
    except ObjectDoesNotExist:
        subscription_id = 0
    context = {
        'username': request.user.username,
        'id': subscription_id,
        'form': form
    }
    return render(request, 'lk.html', context)


def get_recipes_without_allergies(subscription):
    all_allergies = []
    sorted_recipes = []

    milk_allergy = (['Молоко', 'Кефир', 'Творог', 'Сметана', 'Айран',
                     'Бифилин', 'Йогурт', 'Катык', 'Кумыс', 'Кефир',
                     'Масло сливочное', 'Сливочное масло', 'Маргарин',
                     'Мороженое', 'Мацони', 'Молочная сыворотка', 'Пахта', 
                     'Ряженка', 'Сыр', 'Сливки', 'Сгущёное молоко',
                     'Сгущёнка', 'Сгущенка', 'Спред', 'Шубат',
                     'Топлёное масло'])

    fish_allergy = (['Рыбий жир', 'Икр', 'Рыба', 'Сардин', 'Тунец', 'Тунца',
                     'Моллюск', 'Устриц', 'Окунь', 'Микижа', 'Креветк',
                     'Скумбри', 'Треск', 'Пикша', 'Палтус', 'Сайр', 'Минта',
                     'Лосос', 'Нерк', 'Акул', 'Сурими', 'Краб', 'Миди',
                     'Кальмар', 'Чавыч', 'Минта', 'Кет', 'Кильк', 'Окун',
                     'Камбал', 'Хек', 'Сом', 'Форел', 'Шпрот', 'Судак', 'Угр',
                     'Мойв', 'Устрич', 'Дорад', 'Сибас', 'Рыбн', 'Раб'])

    meat_allergy = (['Куриц', 'Курин', 'Мясо', 'Фарш', 'Мясн', 'Говяж', 
                     'Сосиск', 'Сардельк', 'Колбас', 'Козье', 'Бекон', 'Крол',
                     'Зай', 'Теляч', 'Телятин', 'Олен', 'Говядина', 'Язык',
                     'Печень', 'Сало', 'Ветчин', 'Буженин', 'Баранин',
                     'Свинин', 'Индейк'])

    seed_allergy = (['Мука', 'Макарон', 'Спагетти', 'Кукуруз', 'Хлеб', 'Хлоп',
                     'Горош', 'Сухар', 'Тесто', 'Булг', 'Манн','Камут', 'Рож',
                     'Ячмен', 'Полб', 'Лаваш', 'Пшенич', 'Пшениц'])

    honey_allergy = (['Мёд', 'Мед'])

    nuts_allergy = (['Орех', 'Миндал', 'Боб', 'Фасол', 'Горох', 'Нут',
                     'Арахис', 'Люпин', 'Фундук', 'Кешью', 'Фисташк', 'Кедр',
                     'Чечеви'])

    for allergy in subscription.allergies.all():
        if allergy.name == 'Рыба и морепродукты':
             all_allergies += fish_allergy
        if allergy.name == 'Мясо':
            all_allergies += meat_allergy
        if allergy.name == 'Зерновые':
            all_allergies += seed_allergy
        if allergy.name == 'Продукты пчеловодства':
            all_allergies += honey_allergy
        if allergy.name == 'Орехи и бобовые':
            all_allergies += nuts_allergy
        if allergy.name == 'Молочные продукты':
            all_allergies += milk_allergy

    if subscription.subs_type.name == 'Классическое':
        menu_type = 'CL'
    elif subscription.subs_type.name == 'Низкоуглеводное':
        menu_type = 'LC'
    elif subscription.subs_type.name == 'Вегетарианское':
        menu_type = 'VG'
    elif subscription.subs_type.name == 'Кето':
        menu_type = 'KT'
    else:
        menu_type = ''

    recipes = Recipe.objects.filter(menu_type=menu_type)
    
    for recipe in recipes:
        is_append = False

        for ingredient in recipe.ingredients.all():
            is_append = check_for_allergy(ingredient.name, all_allergies)

        if is_append == False:
            sorted_recipes.append(recipe)

    return sorted_recipes


def check_for_allergy(ingredient, allergies):
    fit = False
    for product in allergies:
        if product.lower() in ingredient.lower():
            fit = True
    return fit


@login_required
def subscription_detail(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)

    if not subscription.user == request.user:
        raise Http404

    today = date.today()

    recipes = subscription.recipes.select_related('recipe').filter(date=today)

    if not recipes:
        recipes = random.sample(get_recipes_without_allergies(subscription), subscription.number_of_meals)

        new_recipes = [
            SubscriptionRecipe(
                subscription=subscription,
                recipe=recipe,
                date=today
            )
            for recipe in recipes
        ]

        SubscriptionRecipe.objects.bulk_create(new_recipes)
        recipes = new_recipes

    context = {
        'subscription': subscription,
        'recipes': recipes,
        'date': today
    }

    return render(request, 'subscription.html', context)
