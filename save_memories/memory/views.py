from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Category, Memory
from .forms import MemoryForm
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
        form = MemoryForm(request.POST, request.FILES)
        if form.is_valid():
            memory = form.save(commit=False)
            memory.user = request.user

            category = form.cleaned_data['category']
            new_category_name = form.cleaned_data['new_category_name']

            if category:
                memory.category = category
            elif new_category_name:
                new_category = Category.objects.create(name=new_category_name, user=request.user)
                memory.category = new_category
            memory.save()
            return redirect('memory:gallery')
    else:
        form = MemoryForm()
        form.user = request.user
        form.fields['category'].queryset = categories

    context = {'categories': categories, 'form': form}
    return render(request, 'memory/add.html', context)

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if category.memory_set.count() == 0:
        category.delete()
        return redirect('memory:gallery')
    else:
        return redirect('memory:gallery')

class DeleteMemory(DeleteView):
    model = Memory
    template_name = "memory/delete_remember.html"
    context_object_name = "post"
    success_url = reverse_lazy("memory:gallery")

class UpdateMemory(UpdateView):
    model = Memory  # Используйте модель Memory, а не форму MemoryForm
    form_class = MemoryForm  # Укажите класс вашей формы
    template_name = "memory/add.html"
    success_url = reverse_lazy("memory:gallery")

    def form_valid(self, form):
        memory = form.save(commit=False)
        memory.user = self.request.user

        category = form.cleaned_data['category']
        new_category_name = form.cleaned_data['new_category_name']

        if category:
            memory.category = category
        elif new_category_name:
            new_category = Category.objects.create(name=new_category_name, user=self.request.user)
            memory.category = new_category

        memory.save()
        return super().form_valid(form)