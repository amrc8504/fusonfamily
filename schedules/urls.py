from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm

    def form_valid(self, form):
        remember = form.cleaned_data.get('remember_me')
        if not remember:
            # Session expires when the browser closes
            self.request.session.set_expiry(0)
        else:
            # Session persists (e.g., 2 weeks)
            self.request.session.set_expiry(1209600)  # 2 weeks
        return super().form_valid(form)

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_schedule, name='add_schedule'),
    path('delete/<int:event_id>/', views.delete_schedule, name='delete_schedule'),
    path('edit/<int:event_id>/', views.edit_schedule, name='edit_schedule'),
    path("register/", views.register, name="register"),
    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
]