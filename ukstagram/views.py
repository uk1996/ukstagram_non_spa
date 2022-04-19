from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post
from django.db.models import Q

@login_required
def index(request):
    post_list = Post.objects.filter(Q(author__in=request.user.following_set.all()) | Q(author=request.user))
    suggested_user_list = get_user_model().objects.exclude(pk=request.user.pk)\
                                                  .exclude(pk__in=request.user.following_set.all())[:5]
    return render(request, 'ukstagram/index.html', {
        'post_list':post_list[::-1],
        'suggested_user_list':suggested_user_list,
    })

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag_set.add(*post.extract_tag_list())
            post.caption = post.remove_tag_in_caption()
            post.save()
            messages.success(request, '새로운 포스팅을 작성하였습니다.')
            return redirect(post)
    else:
        form = PostForm()

    return render(request, 'ukstagram/post_form.html', {
        'form':form,
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'ukstagram/post_detail.html', {
        'post':post,
    })


@login_required
def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username,
                                  is_active=True) # 해당 계정이 활성화 되어있을 경우만 접근 가능
    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count() # 실제 데이터베이스에 count 쿼리를 던짐

    if request.user.following_set.filter(pk=page_user.pk).exists():
        is_follow = True
    else:
        is_follow = False

    return render(request, 'ukstagram/user_page.html', {
        'page_user':page_user,
        'post_list':post_list[::-1],
        'post_list_count':post_list_count,
        'is_follow':is_follow,
    })