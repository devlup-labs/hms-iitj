from django.shortcuts import render
from django.views.generic import TemplateView, View


class IndexView(TemplateView):
    template_name = 'main/index.html'


class AddBlog(View):
    def AddBlog(self, request):
        return render(request, 'main/addBlog.html', {})
