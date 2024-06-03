from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'blog/home.html')

def search(request):
    return render(request, 'blog/search.html')

def post_details(request):
    return render(request, 'blog/post_details.html')

def dashboard(request):
    return render(request, 'blog/dashbord/dashbord.html')

def write(request):
    return render(request, 'blog/dashbord/post_write.html')

def drafts(request):
    return render(request, 'blog/dashbord/post_draft.html')

def edit(request):
    return render(request, 'blog/dashbord/post_edit.html')

def published(request):
    return render(request, 'blog/dashbord/post_published.html')

def responses(request):
    return render(request, 'blog/dashbord/responses.html')

def search(request):
    return render(request, 'blog/search.html')