from .forms import PostBlog, EditBlog
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    queryset = BlogPost.objects.filter(published=True)
    template_name = 'blog/blog_list.html'
    context_object_name = 'blog_posts'
    paginate_by = 6


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog_post'


class AddBlogView(CreateView):
	model = BlogPost
	form_class = PostBlog
	template_name = 'dashboard/add_blog.html'

class UpdateBlogView(UpdateView):
	model = BlogPost
	form_class = EditBlog
	template_name = 'dashboard/update_blog.html'

class DeleteBlogView(DeleteView):
	model = BlogPost
	template_name = 'dashboard/delete_blog.html'
	success_url = reverse_lazy('home')
