from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User




def home(request):
    context = {
        # 'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html')



def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
