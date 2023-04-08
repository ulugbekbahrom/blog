from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from django.db.models import Q


class BlogListView(ListView):
    model = Post
    template_name = 'home.html'


class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    

class BlogCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = ['title', 'author', 'body']


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'body']

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    

class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user



def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        posts = Post.objects.filter(
            Q(title__contains=searched) | Q(body__contains=searched)
        )
        return render(request, 'search.html', {'searched': searched, 'posts': posts})
    else:
        return render(request, 'search.html')
        