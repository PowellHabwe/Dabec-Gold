from django.shortcuts import render
from store.models import Product
def home(request):
    home_coins = Product.objects.all().filter(home_coin = True)
    home_bars = Product.objects.all().filter(home_bar = True)
    home_ornaments = Product.objects.all().filter(home_ornament = True)
    home_nuggets = Product.objects.all().filter(home_nugget = True)
    deals = Product.objects.all().filter(deals = True)
    top_rated = Product.objects.all().filter(top_rated = True)
    new = Product.objects.all().filter(new = True)
    best_sellers = Product.objects.all().filter(best_sellers = True)
    context = {
        'home_coins': home_coins,
        'home_bars':home_bars,
        'deals':deals,
        'top_rated':top_rated,
        'new':new,
        'best_sellers':best_sellers,
        'home_ornaments': home_ornaments,
        'home_nuggets':home_nuggets,
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'includes/aboutus.html')