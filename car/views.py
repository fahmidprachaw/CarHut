from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.generic import ListView, DetailView
from .models import Car, Brand, Order
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            register_forms = forms.RegistrationFrom(request.POST)
            if register_forms.is_valid():
                register_forms.save()
                return redirect('login')
        else:
            register_forms = forms.RegistrationFrom()
        return render(request, 'register.html', {'form' : register_forms})
    else:
        return redirect('profile')

def user_login(request):
    if not request.user.is_authenticated:
        print('line 23')
        if request.method == 'POST':
            login_form = AuthenticationForm(request=request, data=request.POST)
            print('line 26')
            if login_form.is_valid():
                name = login_form.cleaned_data['username']
                userpass = login_form.cleaned_data['password']
                user = authenticate(username = name, password = userpass)
                print('line 31')
                if user is not None:
                    print('line 33')
                    login(request, user)
                    return redirect('profile')
        else:
            login_form = AuthenticationForm()
        return render(request, 'register.html', {'form': login_form})
    else:
        return redirect('profile')
    

def user_logout(request):
    logout(request)
    return redirect('login')



def Profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            profile_forms = forms.UserChangeData(request.POST, instance = request.user)
            if profile_forms.is_valid():
                profile_forms.save()
                messages.success(request, 'Saved successfully')
                return redirect('profile')
        else:
            profile_forms = forms.UserChangeData(instance = request.user)
        # return render(request, 'register.html', {'form' : register_forms})
        return render(request, 'profile.html', {'form': profile_forms, 'user': request.user})
    else:
        return redirect('login')
    

class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'

class CarDelailView(DetailView):
    model = Car
    template_name = 'car_detail.html'

    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(self.request.POST)
        car = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.car = car
            new_comment.save()
            return self.get(request, *args, **kwargs)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.object
        comments = car.comments.all()
        comment_form = forms.CommentForm()
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context

@method_decorator(login_required, name='dispatch')
class BuyCarView(DetailView):
    model = Car
    template_name = 'buy_car.html'

    def get(self, request, *args, **kwargs):
        car = self.get_object()
        if car.quantity > 0:
            order = Order.objects.create(user=request.user, car=car)
            car.quantity -= 1
            car.save()
            messages.success(request, f'You have successfully bought {car.name}.')
        else:
            messages.error(request, f'Sorry, {car.name} is out of stock.')
        return redirect('car_detail', pk=car.pk)
    
class OrderHistoryView(ListView):
    model = Order
    template_name = 'order_history.html'
    context_object_name = 'ordered_car'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                # update_session_auth_hash(request, form.cleaned_data['user'])
                return redirect('profile')
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request, 'passchange.html', {'form': form})
    else:
        return redirect('login')


