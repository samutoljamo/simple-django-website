from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from django.views import View

from .models import Post
from . import forms
# Create your views here.


class ProfileView(TemplateView):
    template_name = 'social/profile.html'



class UserDetailView(DetailView):
    model = get_user_model()
    template_name = 'social/user_detail.html'
    context_object_name = 'detail_user'

    def get(self, request, pk):
        if pk == request.user.pk:
            return redirect('profile')
        return super(UserDetailView, self).get(request, pk)


class UserListView(ListView):
    model = get_user_model()
    template_name = 'social/user_list.html'
    context_object_name = 'users'


class PostView(DetailView):
    model = Post
    template_name = 'social/post_detail.html'
    comment_model_form = forms.CreateCommentForm

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['comment_form'] = self.comment_model_form
        return context

    def post(self):
        form = self.comment_model_form(data=self.request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.request
            print(comment.post)
            return self.get(self.request)
        else:
            return self.get(self.request)


class PostDetailView(View):
    model = Post
    template_name = 'social/post_detail.html'
    comment_model_form = forms.CreateCommentForm

    def get(self, request, pk):
        context = self.get_context_data(pk=pk)
        return render(request, self.template_name, context=context)

    def post(self, request, pk):
        context = self.get_context_data(pk=pk)
        form = self.comment_model_form(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = context['post']
            comment.save()
            return self.get(request, pk)
        else:
            context['comment_form'] = form
            return self.get(request, pk)

    def get_context_data(self, **kwargs):
        context = {}
        context['post'] = get_object_or_404(Post, pk=kwargs['pk'])
        context['comment_form'] = self.comment_model_form
        context['comments'] = context['post'].comments.all().order_by('-timestamp')
        return context


class CreatePostView(CreateView):
    model = Post
    fields = ['title', 'body']
    template_name = "social/create_post.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return redirect(post.get_absolute_url())
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for key in form.fields:
            form.fields[key].widget.attrs = {'placeholder': key}
        form.fields['title'].widget.attrs['class'] = 'title'
        form.fields['body'].widget.attrs['class'] = 'resize'
        return form

