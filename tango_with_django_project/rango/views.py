from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.models import Category
from rango.forms import CategoryForm, PageForm


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages = Page.objects.order_by('-views')[:5]

    context_dict={
        'categories': category_list,
        'pages': pages,
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'
    }

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {'cat_image': 'cat.jpg'}
    return render(request, 'rango/about.html', context=context_dict)

def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:index')
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        return redirect('rango:index')

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = form.cleaned_data.get('views', 0)
            page.save()
            return redirect('rango:show_category', category_name_slug=category.slug)
        else:
            print(form.errors)

    return render(request, 'rango/add_page.html', {'form': form, 'category': category})

