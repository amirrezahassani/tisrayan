from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from django.core.paginator import Paginator
from accounts.models import CustomUser
from django.contrib import messages
from .forms import CommentForm
from django.core.mail import send_mail
from portfolio.models import PF


def post_list_view(request):
    posts_list = Post.objects.filter(is_published=True)
    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog.html', {'page_obj': page_obj})


def post_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(approved=True)
    portfolio = PF.objects.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user

            parent_comment_id = request.POST.get('parent_comment_id')
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                if request.user.is_staff:
                    comment.parent = parent_comment
                    send_email_to_user(parent_comment)
                else:
                    messages.error(request, 'شما اجازه پاسخ‌دهی به این کامنت را ندارید.')
                    return redirect(post.get_absolute_url())
            else:
                comment.approved = False

            comment.save()
            messages.success(request, 'کامنت شما با موفقیت ارسال شد.')
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()

    return render(request, 'blog-post.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'portfolio': portfolio,
    })


def send_email_to_user(comment):
    """ارسال ایمیل به کاربر پس از پاسخ ادمین"""
    subject = 'پاسخ به کامنت شما'
    message = f"ادمین به کامنت شما پاسخ داده است: {comment.content}"
    recipient_list = [comment.user.email]
    send_mail(subject, message, 'admin@mysite.com', recipient_list)


def search_view(request):
    query = request.GET.get('s')
    results = Post.objects.filter(title__icontains=query)
    return render(request, 'result.html', {
        'results': results,
        'query': query,
    })
