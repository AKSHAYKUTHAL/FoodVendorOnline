from random import randint
from django.shortcuts import render, get_object_or_404, redirect
from .forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from menu.models import Category, FoodItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vender
from vendor.utils import get_vendor
from menu.forms import CategoryForm, FoodItemForm
from django.template.defaultfilters import slugify



@login_required(login_url='accounts:login')
@user_passes_test(check_role_vender)
def v_profile(request):
    profile = get_object_or_404(UserProfile,user=request.user)
    vendor = get_object_or_404(Vendor,user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'Restaurant has been updated.')
            return redirect('vendor:v_profile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'profile':profile,
        'vendor':vendor,
    }
    return render(request,'vendor/v_profile.html',context)



@login_required(login_url='accounts:login')
@user_passes_test(check_role_vender)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')

    context = {
        'categories':categories,
    }
    return render(request,'vendor/menu_builder.html',context)





@login_required(login_url='accounts:login')
@user_passes_test(check_role_vender)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category,pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)

    context = {
        'fooditems':fooditems,
        'category':category,
    }
    return render(request,'vendor/fooditems_by_category.html',context)



@login_required(login_url='accounts:login')
@user_passes_test(check_role_vender)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            
            # Check if the category with the same name exists for the current vendor
            existing_category = Category.objects.filter(vendor=get_vendor(request), category_name__iexact=category_name).first()
            if existing_category:
                form.add_error('category_name', 'Category with this name already exists.')
            else:
                category = form.save(commit=False)
                category.vendor = get_vendor(request)
                category.slug = slugify(category_name)+'-' + str(request.user.id)
                category.save()
                messages.success(request, 'Category added successfully.')
                return redirect('vendor:menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    context = {
        'form':form,
    }
    return render(request,'vendor/add_category.html',context)





@login_required(login_url='accounts:login')
@user_passes_test(check_role_vender)
def edit_category(request, pk=None):
    category = get_object_or_404(Category,pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)+'-' + str(request.user.id)
            form.save()
            messages.success(request,'Category updated successfully.')
            return redirect('vendor:menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)

    context = {
        'category':category,
        'form':form,
    }
    return render(request,'vendor/edit_category.html', context)





@login_required(login_url='accounts:login')
@user_passes_test(check_role_vender)
def delete_category(request, pk=None):
    category = get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request,'Category has been deleted succesfully')
    return redirect('vendor:menu_builder')







@login_required(login_url='accounts:login')
@user_passes_test(check_role_vender)
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))

        if form.is_valid():
            food_title = form.cleaned_data['food_title']

            existing_food = FoodItem.objects.filter(vendor=get_vendor(request),food_title__iexact=food_title).first()
            if existing_food:
                form.add_error('food_title', 'Food item with this name already exists.')
            else:
                print(food_title)
                food = form.save(commit=False)
                food.vendor = get_vendor(request)
                food.slug = slugify(food_title)+'-' + str(request.user.id)
                form.save()
                messages.success(request,'Food item added successfully.')
                return redirect('vendor:fooditems_by_category',food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm()
        # modify form so only the logged in user categoriesw will be avialable
        # this makes so that, the form will contain only the fields belong to the logged user
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))

    context = {
        'form':form,
    }
    return render(request,'vendor/add_food.html',context)




@login_required(login_url='accounts:login')
@user_passes_test(check_role_vender)
def edit_food(request, pk=None):
    food = get_object_or_404(FoodItem,pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST,request.FILES, instance=food)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title)+'-' + str(request.user.id)
            form.save()
            messages.success(request,'Food item updated successfully.')
            return redirect('vendor:fooditems_by_category',food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm(instance=food)
        
        # modify form so only the logged in user categoriesw will be avialable
        # this makes so that, the form will contain only the fields belong to the logged user
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))

    context = {
        'food':food,
        'form':form,
    }
    return render(request,'vendor/edit_food.html', context)





@login_required(login_url='accounts:login')
@user_passes_test(check_role_vender)
def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem,pk=pk)
    food.delete()
    messages.success(request,'Food Item has been deleted succesfully')
    return redirect('vendor:fooditems_by_category',food.category.id)