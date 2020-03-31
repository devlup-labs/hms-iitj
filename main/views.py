from django.shortcuts import render
from .models import blog
from .forms import AddBlogForm
from django.views.generic import CreateView, TemplateView


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['blogs'] = blog.objects.all()
        return context


def blogDetails(request, pk):
    blogs = blog.objects.get(pk=pk)
    template_name = 'main/blogDetails.html'
    return render(request, template_name, {'blog': blogs})


class AddBlogView(CreateView):
    template_name = 'main/addBlog.html'
    form_class = AddBlogForm
    success_url = '/'
