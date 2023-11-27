from django.shortcuts import render
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect #!
from .forms import UserRegisterForm, UserUpdateForm, UserUpdateImageForm

def register(request) :
    if request.method == 'POST' :
            form = UserRegisterForm(request.POST)
            context = {'form': form}
            if form.is_valid():
                user = form.save()
                created = True
                messages.success(request, f'Account created, you can login now.')
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST' :
        u_form = UserUpdateForm(request.POST, instance=request .user)
        p_form = UserUpdateImageForm(request.POST, request.FILES, instance=request.user)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Acount updated.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserUpdateImageForm(instance=request.user)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request, 'users/profile.html', context)
