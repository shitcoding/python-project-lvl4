from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import View, generic

from task_manager.forms import TaskForm, UserChangeForm, UserCreationForm
from task_manager.models import Label, SiteUser, Status, Task


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """LoginRequiredMixin with custom login page url."""

    login_url = "/login/"


class IndexView(generic.TemplateView):
    """Index page view."""

    template_name = "task_manager/index.html"


# Users
class LoginView(SuccessMessageMixin, auth_views.LoginView):
    """Login page view."""

    next_page = reverse_lazy("index")
    success_message = _("You are logged in")


class SignupView(SuccessMessageMixin, generic.CreateView):
    """Signup page view."""

    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    success_message = _("User created successfully")


class LogoutView(auth_views.LogoutView):
    """Logout page view."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, "You are logged out")
        return super().dispatch(request, *args, **kwargs)


class UserListView(generic.ListView):
    template_name = "task_manager/user_list.html"
    context_object_name = "user_list"

    def get_queryset(self):
        """Return the list of all registered users."""
        return SiteUser.objects.order_by("-signup_date")


class UserUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    UserPassesTestMixin,
    generic.UpdateView,
):
    """User profile update page view."""

    model = SiteUser
    template_name = "registration/user_update.html"

    form_class = UserChangeForm
    success_url = reverse_lazy("users")
    success_message = _("User info changed successfully")

    def get_context_data(self, **kwargs):
        """Add password change form to page context."""
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context["password_change_form"] = auth_views.PasswordChangeForm(
            user=self.request.user,
        )
        return context

    def test_func(self):
        """Check if user have permissions to update profile."""
        target_user = self.get_object()
        return (
            target_user == self.request.user or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        messages.error(
            self.request,
            "You have no permissions to change other user",
        )
        return redirect(reverse_lazy("users"))


class UserDeleteView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    UserPassesTestMixin,
    generic.DeleteView,
):
    """User deletion page view."""

    model = SiteUser
    template_name = "registration/user_delete.html"

    success_url = reverse_lazy("users")
    success_message = _("User deleted successfully")

    def test_func(self):
        """Check if user have permissions to delete profile."""
        target_user = self.get_object()
        return (
            target_user == self.request.user or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("You have no permissions to change other user"),
        )
        return redirect(reverse_lazy("users"))


# Tasks
class TaskListView(CustomLoginRequiredMixin, generic.ListView):
    """Tasks list page view."""

    template_name = "task_manager/task_list.html"
    context_object_name = "task_list"

    def get_queryset(self):
        """Return the list of all tasks."""
        return Task.objects.order_by("-created_on")


class TaskCreateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView,
):
    """Task creation page view."""

    model = Task
    form_class = TaskForm
    template_name = "task_manager/task_create_form.html"
    success_url = reverse_lazy("tasks")
    success_message = _("Task created successfully")

    def form_valid(self, form):
        task = form.save(commit=False)
        task.creator = self.request.user
        task.save()
        return super().form_valid(form)


class TaskDetailView(CustomLoginRequiredMixin, generic.DetailView):
    """Task detail page view."""

    model = Task
    template_name = "task_manager/task_detail.html"


class TaskUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """Task update page view."""

    model = Task
    form_class = TaskForm
    template_name = "task_manager/task_update_form.html"
    success_url = reverse_lazy("tasks")
    success_message = _("Task updated successfully")


class TaskDeleteView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    UserPassesTestMixin,
    generic.DeleteView,
):
    """Task delete page view."""

    model = Task
    template_name = "task_manager/task_delete.html"

    success_url = reverse_lazy("tasks")
    success_message = _("Task deleted successfully")

    def test_func(self):
        """Check if user have permissions to delete the task."""
        task_creator = self.get_object().creator
        return (
            task_creator == self.request.user or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        messages.error(
            self.request,
            _(
                "You have no permissions to delete the task created by other user"
            ),
        )
        return redirect(reverse_lazy("tasks"))


# Statuses
class StatusListView(CustomLoginRequiredMixin, generic.ListView):
    """Statuses list page view."""

    template_name = "task_manager/status_list.html"
    context_object_name = "status_list"

    def get_queryset(self):
        """Return the list of all statuses."""
        return Status.objects.order_by("-created_on")


class StatusCreateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView,
):
    """Status creation page view."""

    template_name = "task_manager/status_create_form.html"
    model = Status
    fields = ["name"]
    success_url = reverse_lazy("statuses")
    success_message = _("Status created successfully")


class StatusUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """Status update page view."""

    template_name = "task_manager/status_update_form.html"
    model = Status
    fields = ["name"]
    success_url = reverse_lazy("statuses")
    success_message = _("Status updated successfully")


class StatusDeleteView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    """Status deletion page view."""

    template_name = "task_manager/status_delete_form.html"
    model = Status
    success_url = reverse_lazy("statuses")
    success_message = _("Status deleted successfully")


# Labels
class LabelListView(CustomLoginRequiredMixin, generic.ListView):
    template_name = "task_manager/label_list.html"
    context_object_name = "label_list"

    def get_queryset(self):
        """Return the list of all labels."""
        return Label.objects.order_by("-created_on")


class LabelCreateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView,
):
    """Label creation page view."""

    template_name = "task_manager/label_create.html"
    model = Label
    fields = ["name"]
    success_url = reverse_lazy("labels")
    success_message = _("Label created successfully")


class LabelUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """Label update page view."""

    template_name = "task_manager/label_update.html"
    model = Label
    fields = ["name"]
    success_url = reverse_lazy("labels")
    success_message = _("Label updated successfully")


class LabelDeleteView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    """Label deletion page view."""

    template_name = "task_manager/label_delete.html"
    model = Label
    success_url = reverse_lazy("labels")
    success_message = _("Label deleted successfully")
