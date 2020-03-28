from django.shortcuts import render, redirect
from .models import blog
from .forms import AddBlogForm


def IndexPage(request):
    template_name = 'main/index.html'
    blogs = blog.objects.all()
    return render(None, template_name, {'blogs': blogs})


def blogDetails(request, pk):
    blogs = blog.objects.get(pk=pk)
    template_name = 'main/blogDetails.html'
    return render(request, template_name, {'blog': blogs})


def AddBlogView(request):
    template_name = 'main/addBlog.html'
    if request.method == "POST":
        f = AddBlogForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('main:home')
    else:
        f = AddBlogForm()
    return render(request, template_name, {'form': f})
