from django.contrib import messages
from django.db import transaction
from django.shortcuts import *
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.decorators import *
from .models import *


@csrf_exempt
def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid() and form.clean_username() and form.clean():
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    email=None,

                )
                authenticate(username=user.username, password=user.password)
                login(request,user)
                return HttpResponseRedirect('update_profile/')
            else:
                return render(request, 'logout.html')
        else:
            form = SignupForm()
            variables = RequestContext(request, {'form': form})

            return render_to_response(
                'signup.html',
                variables,
            )
    else:
        return HttpResponseRedirect('/')


@login_required(login_url="login/")
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('update_profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'user_form': user_form,'profile_form': profile_form}
                  )


@login_required(login_url="login/")
def home(request):
    players = User.objects.filter(profile__type__exact=1)
    return render(request, "dashboard.html", {'user': players})


@login_required(login_url="login/")
def transact_money(request):
    if request.method == 'POST':
        user_money = request.user.profile.money
        giving_money = request.POST.get('money')
        if user_money >= giving_money:
            user_money -= giving_money
            player = giving_money
            player.profile.money += giving_money
            return HttpResponseRedirect('scoreboard')
        else:
            messages.error(request, ('Please correct the error below.'))
            transaction_form = TransactionForm
            return render(request, 'transaction.html', {'transaction_form': transaction_form})
    else:
        transaction_form = TransactionForm
        return render(request, 'transaction.html', {'transaction_form': transaction_form})



def scoreboard(request):
    players = User.objects.filter(profile__type__exact=1)
    return render(request, 'scoreboard.html', {'players': players})


@login_required(login_url="login/")
def logout_view(request):
    logout(request)
    return render(request, "logout.html")
