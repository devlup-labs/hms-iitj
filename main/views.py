from django.shortcuts import render
from .models import blog
from .forms import AddBlogForm
from django.views.generic import CreateView


def IndexPage(request):
    template_name = 'main/index.html'
    blogs = blog.objects.all()
    return render(None, template_name, {'blogs': blogs})


def blogDetails(request, pk):
    blogs = blog.objects.get(pk=pk)
    template_name = 'main/blogDetails.html'
    return render(request, template_name, {'blog': blogs})


class AddBlogView(CreateView):
    template_name = 'main/addBlog.html'
    form_class = AddBlogForm
    success_url = '/'
