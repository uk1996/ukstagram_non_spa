from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post, Tag

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