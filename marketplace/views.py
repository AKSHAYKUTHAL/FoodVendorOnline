from django.shortcuts import get_object_or_404, render
from .context_processors import get_cart_counter
from vendor.models import Vendor
from menu.models import Category,FoodItem
from django.db.models import Prefetch
from django.http import HttpResponse,JsonResponse
from .models import Cart


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors':vendors,
        'vendor_count':vendor_count,
    }
    return render(request,'marketplace/listings.html',context)




def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor,vendor_slug=vendor_slug)
    
    # Accessing the food items from the category model using related name "fooditems" in the menu models
    # this way you can access the fooditems related to the category even when the category is not a foreignkey of Category table
    # And its called reverse lookup
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
    }
    return render(request,'marketplace/vendor_detail.html',context)




def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        # check if its ajax request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added the food to the cart
                try:
                    check_cart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # increase cart quantity
                    check_cart.quantity += 1
                    check_cart.save()
                    return JsonResponse({'status':'Success','message':'Added one more of the same food item to the cart.','cart_counter':get_cart_counter(request), 'qty':check_cart.quantity})
                # if the user havn't already added the food to the cart the create the cart
                except:
                    check_cart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status':'Success','message':'Added the food to the cart.','cart_counter':get_cart_counter(request), 'qty':check_cart.quantity})
            except:
                return JsonResponse({'status':'Failed','message':'This food does not exist.'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request'})
    else: 
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
    



def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        # check if its ajax request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added the food to the cart
                try:
                    check_cart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if check_cart.quantity > 1 :
                        # decrease  cart quantity
                        check_cart.quantity -= 1
                        check_cart.save()
                    else:
                        check_cart.delete()
                        check_cart.quantity = 0
                    return JsonResponse({'status':'Success','cart_counter':get_cart_counter(request), 'qty':check_cart.quantity})
                # if the user havn't already added the food to the cart the create the cart
                except:
                    return JsonResponse({'status':'Failed','message':'You do not have this food in your cart.'})
            except:
                return JsonResponse({'status':'Failed','message':'This food does not exist.'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request'})
    else: 
        return JsonResponse({'status':'login_required','message':'Please login to continue'})