from django.shortcuts import render, redirect
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .models import Category, Memory
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def index(request):
    return render(request, 'registration/index.html')

def registration(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('memory:login')
    context = {"form": form}
    return render(request, 'registration/registration.html', context=context)

@login_required
def gallery(request):
    user_memories = Memory.objects.filter(user=request.user)
    user_categories = Category.objects.filter(user=request.user)
    category = request.GET.get('category')
    if category == None:
        memories = user_memories.all()
    else:
        memories = user_memories.filter(category__name=category)

    categories = user_categories
    context = {'categories': categories, 'memories': memories}
    return render(request, 'memory/gallery.html', context)

@login_required
def viewRemembering(request, pk):
    memory = Memory.objects.get(id=pk)
    return render(request, 'memory/remembering.html', {'memory': memory})

@login_required
def addMemory(request):
    categories = Category.objects.filter(user=request.user)

    if request.method == "POST":
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'], user=request.user)
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'], user=request.user)
        else:
            category = None
        
        address = data.get('address', '')
        latitude, longitude = data.get("latitude", ""), data.get("longitude", "")

        memory = Memory.objects.create(
            user=request.user,
            category=category,
            description=data['description'],
            latitude=latitude,
            longitude=longitude,
            address=address,
            image=image,
        )

        return redirect('memory:gallery')

    context = {'categories': categories}
    return render(request, 'memory/add.html', context)

class DeleteMemory(DeleteView):
    model = Memory
    template_name = "memory/delete_remember.html"
    context_object_name = "post"
    success_url = reverse_lazy("memory:gallery")