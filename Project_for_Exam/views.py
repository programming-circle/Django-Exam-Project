from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpRequest, HttpResponseNotAllowed


# Auth libraries here:
from django.contrib.auth import login , logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required , user_passes_test
from .forms import RegistationForm, CarCreateForm 
from .models import MyUser , Cars, Brand
# ------------- Auth section ----------------
 

def register_page( request: HttpRequest):
    return render(request, "register.html", {"form": RegistationForm})

def register_view(request: HttpRequest):
    if request.method == "POST":
        form = RegistationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("auth_page")
        else: return redirect("register_page")
    return HttpResponseNotAllowed(["POST",])
def login_page(request:HttpRequest):
    if request.user.is_authenticated : return redirect("auth_page")
    return render(request, "register.html", {"form":AuthenticationForm,
                                            "button":"Login","action":"login-view"})

def login_view(request: HttpRequest):
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("auth_page")
        else: return redirect("login_page")
    return HttpResponseNotAllowed(["POST",])


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("login_page")

@login_required
def auth_page(request:HttpRequest):
    return render(request, "auth.html", {"user":request.user})

#------ AdminPanel dashboard 

def if_staff_user(user:MyUser):
    return user.is_staff

#I decide to make one big method for rendering dashboard and forms on it.
# user_passes_test - special library shortcut method for testing if user logined , first parameter goes to If_staff_user 
# and checks if he staff and if no sends him to login page for autorization.
@user_passes_test(if_staff_user, login_url='login_page')
def staff_dashboard(request):
    empty_form = CarCreateForm()

    if request.method == "POST":
        action = request.POST.get('action')
        # Create
        if action == "create":
            create_form = CarCreateForm(request.POST)
            if create_form.is_valid():
                create_form.save()
                return redirect('dashboard')
            else:
                print("--- ОШИБКА СОЗДАНИЯ МАШИНЫ ---")
                print(create_form.errors)
                empty_form = create_form

        # Update
        elif action == "update":
            car_id = request.POST.get('product_id')
            car = get_object_or_404(Cars, id=car_id)
            form = CarCreateForm(request.POST, instance=car)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
            else:
                print("--- ОШИБКА СОЗДАНИЯ МАШИНЫ ---")
                print(form.errors)
        # Delete   
        elif action == "delete":
            car_id = request.POST.get('product_id')
            car = get_object_or_404(Cars, id=car_id)
            car.delete()
            return redirect('dashboard')
        
    # Get is always working without clicking on action.
    cars = Cars.objects.all() 
    # search things
    search_query = request.GET.get('search', '') #for searching stuff
    if search_query:
        cars = cars.filter(name__icontains=search_query)
   
    context = {
        "cars": cars,
        "search_query": search_query,
        "empty_form": empty_form,
        "brands": Brand.objects.all(),
    }
    
    return render(request, "dashboard.html", context)

# #Update
# @user_passes_test(if_staff_user, login_url='login')
# def staff_product_update(request, id):
#     car = get_object_or_404(Cars,id=id)
#     if request.method == "POST":
#         form = ProductForm(request.POST, instance=car) 
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#     else:
#         form = ProductForm(instance=car)
#     return render(request, "staff/product_form.html", {"form": form, "title": "Updating"})

# Create your views here.