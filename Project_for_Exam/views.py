from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpRequest, HttpResponseNotAllowed
from django.contrib import messages
#from django.db.models.functions import Lower

# Auth libraries here:
from django.contrib.auth import login , logout , get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required , user_passes_test
from .forms import RegistationForm, CarCreateForm 
from .models import MyUser , Cars, Brand
# ------------- Auth section ----------------
 

def register_page(request: HttpRequest):
    if request.method == "POST":
        form = RegistationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main_page")
        return render(request, "register.html", {"form": form})

    return render(request, "register.html", {"form": RegistationForm()})

def register_view(request: HttpRequest):
    if request.method == "POST":
        form = RegistationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main_page")
        return render(request, "register.html", {"form": form})
    return HttpResponseNotAllowed(["POST",])

def login_page(request:HttpRequest):
    if request.user.is_authenticated : return redirect("main_page")
    return render(request, "register.html", {"form": AuthenticationForm(),
                                            "button":"Login","action":"login-view"})

def login_view(request: HttpRequest):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("main_page")
        else: 
            error_text = form.non_field_errors().as_text()
            if not error_text:
                error_text = "; ".join(
                    f"{field}: {' '.join(errors)}"
                    for field, errors in form.errors.items()
                )
            if error_text:
                error_text = error_text.lstrip('* ').strip()
            else:
                error_text = "Invalid username or password. Please try again."
            messages.error(request, error_text)
            return render(request, "register.html", {"form": form, "button": "Login"})
            
    return HttpResponseNotAllowed(["POST",])


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("login_page")



# Car page

@login_required(login_url='login_page')
def car_purchase(request, slug):
    car = get_object_or_404(Cars, slug=slug)
    return render(request, 'car_purchase.html', {'car': car})

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
            create_form = CarCreateForm(request.POST, request.FILES)
            if create_form.is_valid():
                car = create_form.save(commit=False)

                image = request.FILES.get('image')
                if image:
                    car.image_path = image

                car.save()
                return redirect('dashboard')
            else:
                print("--- ОШИБКА СОЗДАНИЯ МАШИНЫ ---")
                print(create_form.errors)
                empty_form = create_form

        # Update
        elif action == "update":
            car_id = request.POST.get('product_id')
            car = get_object_or_404(Cars, id=car_id)
            form = CarCreateForm(request.POST, request.FILES, instance=car)
            if form.is_valid():
                car = form.save(commit=False)

                image = request.FILES.get('image')
                if image:
                    car.image_path = image
                car.save()
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


def main(request):
    cars = Cars.objects.all()

    selected_brand_id = request.GET.get('brand', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    search_query = request.GET.get('search', '').strip()
    sort_order = request.GET.get('sort', '') 

    if selected_brand_id:
        cars = cars.filter(brand_id=selected_brand_id)

    if price_min:
        cars = cars.filter(price__gte=price_min)

    if price_max:
        cars = cars.filter(price__lte=price_max)

    if search_query:
        cars = cars.filter(name__icontains=search_query)

    if sort_order == 'price_asc':
        cars = cars.order_by('price')      
    elif sort_order == 'price_desc':
        cars = cars.order_by('-price')     

    context = {
        "cars": cars,
        "brands": Brand.objects.all(),
        "selected_brand_id": selected_brand_id,
        "price_min": price_min,
        "price_max": price_max,
        "search_query": search_query,
        "sort_order": sort_order,
    }
    return render(request, "main.html", context)


# @user_passes_test()

# Create your views here.