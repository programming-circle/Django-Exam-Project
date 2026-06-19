from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpRequest, HttpResponseNotAllowed
from django.contrib import messages
#from django.db.models.functions import Lower
from .forms import RegistationForm, CarCreateForm, BrandForm

# Auth libraries here:
from django.contrib.auth import login , logout , get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required , user_passes_test
from .forms import RegistationForm, CarCreateForm , OrderForm
from .models import MyUser , Cars, Brand , Order ,ColorPalette
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

def order(request:HttpRequest, slug: str):
    car = get_object_or_404(Cars, slug=slug)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user_ID = request.user.id

            hex_color = request.POST.get('chosen_color', '#1A237E').lstrip('#')
            # Convert HEX to RGB
            try:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
            except Exception:
                r, g, b = (26, 35, 126)  # fallback color

            color_obj, created = ColorPalette.objects.get_or_create(
                red=r, green=g, blue=b
            )
            order.chosen_color = color_obj
            order.car = car
            order.save()
            context = {
                "message": "Order succesfully created",
                "car": car,
                "form": OrderForm(),
            }
            return render(request, "car_purchase.html", context)

        
        return render(request, "car_purchase.html", {"car": car, "form": form})

    
    form = OrderForm()
    return render(request, "main.html", {"car": car, "form": form})



#------ AdminPanel dashboard 

def if_staff_user(user:MyUser):
    return user.is_staff

#I decide to make one big method for rendering dashboard and forms on it.
# user_passes_test - special library shortcut method for testing if user logined , first parameter goes to If_staff_user 
# and checks if he staff and if no sends him to login page for autorization.


@user_passes_test(if_staff_user, login_url='login_page')
def staff_dashboard(request):
    empty_car_form = CarCreateForm()
    empty_brand_form = BrandForm()
    empty_user_form = RegistationForm()

    if request.method == "POST":
        action = request.POST.get('action')
        
        #method for creating a model for car
        if action == "create":
            create_form = CarCreateForm(request.POST, request.FILES)
            if create_form.is_valid():
                car = create_form.save(commit=False)
                image = request.FILES.get('image')
                if image: car.image_path = image
                car.save()
                return redirect('dashboard')
            else:
                empty_car_form = create_form
        #update car model
        elif action == "update":
            car_id = request.POST.get('product_id')
            car = get_object_or_404(Cars, id=car_id)
            form = CarCreateForm(request.POST, request.FILES, instance=car)
            if form.is_valid():
                car = form.save(commit=False)
                image = request.FILES.get('image')
                if image: car.image_path = image
                car.save()
                return redirect('dashboard')
        # delete car model
        elif action == "delete":
            car_id = request.POST.get('product_id')
            car = get_object_or_404(Cars, id=car_id)
            car.delete()
            return redirect('dashboard')

        #method for creating a brand for car
        elif action == "create_brand":
            brand_form = BrandForm(request.POST)
            if brand_form.is_valid():
                brand_form.save()
                return redirect('dashboard')
            else:
                empty_brand_form = brand_form
        #update brand
        elif action == "update_brand":
            brand_id = request.POST.get('brand_id')
            brand = get_object_or_404(Brand, id=brand_id)
            form = BrandForm(request.POST, instance=brand)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        #delete brand
        elif action == "delete_brand":
            brand_id = request.POST.get('brand_id')
            brand = get_object_or_404(Brand, id=brand_id)
            brand.delete()
            return redirect('dashboard')

        #method for creating a model for user
        elif action == "create_user":
            user_form = RegistationForm(request.POST)
            if user_form.is_valid():
                user_form.save()
                return redirect('dashboard')
            else:
                empty_user_form = user_form
        #update user model
        elif action == "update_user":
            user_id = request.POST.get('user_id')
            user_obj = get_object_or_404(MyUser, id=user_id)
            form = RegistationForm(request.POST, instance=user_obj)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        #delete user model
        elif action == "delete_user":
            user_id = request.POST.get('user_id')
            user_obj = get_object_or_404(MyUser, id=user_id)
            if user_obj != request.user:
                user_obj.delete()
            return redirect('dashboard')
        
    cars = Cars.objects.all() 
    users = MyUser.objects.all()
    brands = Brand.objects.all()

    #method for searchings for filter
    search_query = request.GET.get('search', '') #getting from main site info and searching by is.
    if search_query:
        cars = cars.filter(name__icontains=search_query)
        users = users.filter(full_name__icontains=search_query)
        brands = brands.filter(name__icontains=search_query)
   
    context = {
        "cars": cars,
        "brands": brands,
        "users": users,
        "search_query": search_query,
        "empty_car_form": empty_car_form,
        "empty_brand_form": empty_brand_form,
        "empty_user_form": empty_user_form,
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