from django.shortcuts import render, redirect
from blog.models import Post
from django.core.mail import send_mail
from .forms import ContactForm


def index(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')[:4]
    return render(request, 'index.html', {'posts': posts})


def services(request):
    return render(request, 'services.html')


def web_design(request):
    return render(request, 'service-web.html')


def socialmedia_admin(request):
    return render(request, 'service-admin.html')


def content_creator(request):
    return render(request, 'service-content.html')


def graphic_design(request):
    return render(request, 'service-design.html')


def seo(request):
    return render(request, 'service-seo.html')


def rules(request):
    return render(request, 'rules.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            send_mail(
                'پیام شما دریافت شد',
                f'سلام {name},\n\nپیام شما دریافت شد. ما به زودی با شما تماس خواهیم گرفت.',
                'info@tisweb.ir',
                [email],
                fail_silently=False,
            )
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact-us.html', {'form': form})


def custom_page_not_found_view(request, exception):
    return render(request, "404.html", {})
