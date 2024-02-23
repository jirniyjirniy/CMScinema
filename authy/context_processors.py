from .forms import LoginAjaxForm


def get_context_data(request):
    context = {
        'login_ajax': LoginAjaxForm()
    }
    return context