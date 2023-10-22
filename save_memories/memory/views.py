from django.shortcuts import render, redirect
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .models import Category, Memory


def gallery(request):
    category = request.GET.get('category')
    if category == None:
        memories = Memory.objects.all()
    else:
        memories = Memory.objects.filter(category__name=category)

    categories = Category.objects.all()
    context = {'categories': categories, 'memories': memories}
    return render(request, 'memory/gallery.html', context)


def viewRemembering(request, pk):
    memory = Memory.objects.get(id=pk)
    return render(request, 'memory/remembering.html', {'memory': memory})


def addMemory(request):
    categories = Category.objects.all()

    if request.method == "POST":
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        memory = Memory.objects.create(
            category=category,
            description = data['description'],
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