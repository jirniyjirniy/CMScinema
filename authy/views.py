from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View

from .forms import LoginAjaxForm, RegisterForm
from .models import CustomUser


class RegisterAjaxView(View):
    template_name = 'user/register_done.html'

    def get(self, request):
        user_form = RegisterForm()
        return render(request, 'user/register.html', {'user_form': user_form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            language = request.POST.get('language')
            city = request.POST.get('city')
            phone = request.POST.get('phone')
            birth_date = request.POST.get('birth_date')
            password = request.POST.get('password')

            try:
                user = User.objects.create_user(username=username, email=email, password=password,
                                                first_name=first_name, last_name=last_name)
                new_user = CustomUser.objects.create(user=user, nickname=username, email=email, name=first_name,
                                                     second_name=last_name, gender=gender, language=language,
                                                     birth_date=birth_date, city=city, phone_number=phone)
                login(request, user)
                success_html = render(request, 'user/register_done.html').content.decode('utf-8')
                response_data = {'success': True, 'html': success_html}
                return JsonResponse(response_data, safe=False)
            except Exception as e:
                errors = {'status': False, 'errors': {'non_field_errors': [str(e)]}}
                return JsonResponse(errors)
        else:
            errors = {'status': False, 'errors': form.errors}
            return JsonResponse(errors)


def logout_view(request):
    logout(request)
    return redirect('cinema:index')


class LoginAjaxView(View):
    template_name = 'user/login_success.html'

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                success_html = render(request, self.template_name).content.decode('utf-8')
                response_data = {'success': True, 'html': success_html}
                return JsonResponse(response_data, safe=False)
            else:
                response_data = {'error': 'Логин или пароль указаны неверно'}
                return JsonResponse(response_data)

        response_data = {'error': 'Логин или пароль не указан'}
        return JsonResponse(response_data)


def single_login(request):
    return render(request, 'user/single_login.html')
