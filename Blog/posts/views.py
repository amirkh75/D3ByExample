from django.core import paginator
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count


from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

class PostListView(ListView):

    def get_queryset(self):
        if self.kwargs:
            self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
            return Post.published.all().filter(tags__in=[self.tag])
        else:
            return Post.published.all()


    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'posts/post/list.html'


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

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status='published', publish__year=year, publish__month=month, publish__day=day , slug=post)
    
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm(initial={'name': f'{request.user.profile.first_name}','email': f'{request.user.email}'})
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'posts/post/detail.html',{'post': post,'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form, 'similar_posts': similar_posts}) 


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s email is: {cd['email']} \n\n {cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'python.codes.site@gmail.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm(initial={'name': f'{request.user.profile.first_name} {request.user.profile.last_name}','email': request.user.email})
    return render(request, 'posts/post/share.html',{'post': post, 'form': form, 'sent':sent})

