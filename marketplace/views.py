from django.shortcuts import get_object_or_404, render
from vendor.models import Vendor
from menu.models import Category,FoodItem
from django.db.models import Prefetch


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

    context = {
        'vendor':vendor,
        'categories':categories,
    }
    return render(request,'marketplace/vendor_detail.html',context)