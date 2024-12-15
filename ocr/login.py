from .forms import LoginForm
from .models import OCRUser


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if OCRUser.objects.filter(username=username, password=password):
                return username
        else:
            return None

    return None
