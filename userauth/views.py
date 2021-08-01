from django.shortcuts import redirect, render
from .forms import CustomUserCreatorForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    return render(request,"user/dashboard.html")


def register_user(request):
   
    if request.method == 'GET':  
        context = {'form':CustomUserCreatorForm()}
        return render(request,'registration/register.html',context)
    
    elif request.method == 'POST':
        form = CustomUserCreatorForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.save()
            messages.success(request,"Your account has been created successfully")
            return redirect('home')
        else:
            messages.error(request,"Invalid details, please fill the form correctly")
            context = {'form':form}
            return render(request,'registration/register.html',context)

def view(request):
    return render(request,"hr/view.html")

