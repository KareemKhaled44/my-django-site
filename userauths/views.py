from django.http import HttpResponse
from django.shortcuts import render
from userauths.forms import UserRegistrationForm
from django.contrib.auth.views import PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
from userauths.models import User
from core.models import Category
from django.contrib.auth.hashers import check_password
# Create your views here.
def register_view(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        # Check if the form is valid
        if form.is_valid():
            new_user=form.save()
            # Authenticate the user
            new_user= authenticate(
                  email=form.cleaned_data.get('email'),
                  password=form.cleaned_data.get('password1')
            )
            # Log the user in
            login(request, new_user)
            messages.success(request, 'you have registered successfully')
            return redirect('core:index') # Redirect to the sign in page after successful registration
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
        'categories': categories,
        }  
    return render(request, 'userauths/sign-up.html', context)

def login_view(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('core:index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have logged in successfully')
                return redirect('core:index')
            else:
                messages.error(request, 'User does not exist or password is incorrect')
                return redirect('userauths:sign-in')
        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist')
            return redirect('userauths:sign-in')
        
        
    return render(request, 'userauths/sign-in.html', {
        'categories': categories,
    })

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('userauths:sign-in')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def get_success_url(self):
        return reverse_lazy('userauths:sign-in')  

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Your password has been reset. You can now log in.")
        return super().dispatch(request, *args, **kwargs)
    

