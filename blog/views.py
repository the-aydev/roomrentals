from django.views.generic import ListView, DetailView

from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    queryset = BlogPost.objects.filter(published=True)
    template_name = 'blogpost_list.html'
    context_object_name = 'blog_posts'
    paginate_by = 6


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_detail.html'
    context_object_name = 'blog_post'
