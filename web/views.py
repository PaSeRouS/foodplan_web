from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .forms import RegisterForm
from .models import Allergy, SubscriptionType, Subscription


def order(request):
    if request.method == 'POST':
        user = User.objects.get(username='admin')

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

        return render(request, 'index.html')
    else:
        context = {
            'allergies': [allergy.name for allergy in Allergy.objects.all()]
        }

        return render(request, 'order.html', context)


def register(request):
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
