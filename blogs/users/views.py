from django.shortcuts import render,redirect
from django.contrib import messages
from .form import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method =='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'your account is created!')
            return redirect('login')

    else:
        form=UserRegisterForm()
    return render(request,'users/register.html',{'form':form})
    

class CustomLogoutView(LogoutView):
    template_name = 'users/log_out.html'


@login_required
def profile(request):
      if request.method =='POST':
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'your account has been updated!')
            return redirect('profile')

      else:
           u_form=UserUpdateForm(instance=request.user)
           p_form=ProfileUpdateForm(instance=request.user.profile)

      context={
        'u_form':u_form,
        'p_form':p_form
    }
      return render(request,'users/profile.html',context)
