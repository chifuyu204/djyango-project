from django.shortcuts import render,HttpResponse,get_object_or_404
from django.contrib.auth.models import User
from .models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

# Create your views here.
def home(request):
   context={
       'post':Post.objects.all()
   }
   return render(request,'blog/home.html',context)


class PostListView(ListView):
    model=Post
    template_name='blog/home.html'
    context_object_name='post'
    ordering=['-date_posted']
    paginate_by=5

class UserPostListView(ListView):
    model=Post
    template_name='blog/user_posts.html'
    context_object_name='post'
    paginate_by=5

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
class PostDetailView(DetailView):
    model=Post
    template_name = 'blog/post_detail.html'  # Update this line
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','content']
    template_name = 'blog/post_form.html'  # Update this line
    context_object_name = 'post'
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
class PostUpdateListView( LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title','content']
    template_name = 'blog/post_form.html'  # Update this line
    context_object_name = 'post'
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
    
class PostDeleteView( LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model=Post
    template_name = 'blog/post_confirm_delete.html'  # Update this line
    context_object_name = 'post'
    success_url='/'
    
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False

    
def about(request):
    return render(request,'blog/about.html',{'title':'About'})


