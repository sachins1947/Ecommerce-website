from django.shortcuts import render
from store.models import Product
from category.models import Category

def home(request):
    caretorys = Category.objects.all()
    # products = Product.objects.all().filter(is_available=True)

    context = {
        'caretorys': caretorys,
    }
    
    return render(request, 'home.html', context)