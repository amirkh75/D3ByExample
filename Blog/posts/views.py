from django.core import paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
import sys
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.views import View

from users.models import CustomUser

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm, PostCreateForm


class PostListView(LoginRequiredMixin, ListView):
    login_url = 'users:login'

    def get_queryset(self):
        if self.kwargs:
            self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
            return Post.published.all().filter(tags__in=[self.tag])
        else:
            return Post.published.all()


    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'posts/post/list.html'

class UserPostListView(LoginRequiredMixin, ListView): 
    """All post from a certain user"""
    login_url = 'users:login'

    def get_queryset(self):
        user = CustomUser.objects.get(id=self.kwargs['user_id'])
        return Post.published.filter(author=user)


    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'posts/post/list.html'

class UserCommentedPostListView(LoginRequiredMixin, ListView):
    """All post Commented from a certain user"""
    login_url = 'users:login'

    def get_queryset(self):
        user = CustomUser.objects.get(id=self.kwargs['user_id'])
        return Comment.objects.filter(author=user)


    context_object_name = 'comments'
    paginate_by = 3
    template_name = 'posts/post/commentedPostList.html'

@login_required
def post_list(request):
    objects_list = Post.published.all()
    paginator = Paginator(objects_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) # if out of the range deliver last page instead.
    return render(request, 'posts/post/list.html', {'page': page, 'posts': posts})


@login_required
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status='published', publish__year=year, publish__month=month, publish__day=day , slug=post)
    
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    objects_list = post.comments.filter(active=True).order_by('id')
    paginator = Paginator(objects_list, 4)
    page = request.GET.get('page', 1)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages) # if out of the range deliver last page instead.
    print(sys.stderr, page)

    
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'posts/post/detail.html',
                    {'post': post,'comments': comments,
                     'new_comment': new_comment, 'comment_form': comment_form,
                      'similar_posts': similar_posts,'page': page}) 



@login_required
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{request.user.email} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {request.user.profile.first_name}\'s email is: {request.user.email} \n\n {request.user.email}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'python.codes.site@gmail.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm(initial={'name': f'{request.user.profile.first_name} {request.user.profile.last_name}','email': request.user.email})
    return render(request, 'posts/post/share.html',{'post': post, 'form': form, 'sent':sent})



@login_required
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            #search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            #search_query = SearchQuery(query)
            #results = Post.published.annotate(
            #    search=search_vector,
            #    rank=SearchRank(search_vector, search_query)
            #).filter(rank__gte=0.3).order_by('-rank')
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')
    return render(request,
                  'posts/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


class PostCreateView(LoginRequiredMixin, View):
    """Create new post"""
    form_class = PostCreateForm
    template_name = 'posts/post/create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            post_ = form.save(commit=False)
            post_.date_modified = datetime.now()
            post_.created = datetime.now()
            post_.updated = datetime.now()
            post_.status = 'published'
            post_.author = request.user
            post_.save()
            return redirect(post_.get_absolute_url())  

        return render(request, self.template_name, {'form': form})