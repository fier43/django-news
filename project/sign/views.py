from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/index.html'


from django.views import View
from django.contrib.auth.forms import AuthenticationForm

class LoginFormView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'sign/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            # Добавьте свою логику для обработки введенных данных формы
            return render(request, 'success.html')
        return render(request, 'sign/login.html', {'form': form})


class CommonRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')
