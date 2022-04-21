from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .models import Task


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

    pass


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')

        return super(RegisterPage, self).get(*args, **kwargs)
    pass


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['color'] = 'red'
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__icontains =search_input) # i get error here
            # context['tasks'] = context['tasks'].filter(
            #     title__startswith =search_input) # i get error here

        context['search_input'] = search_input
        return context
    pass


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"
    template_name = "base/task.html"
    pass


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    # field = ['title','description','complete']
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

    pass


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    pass


class TaskDelte(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"  # by default context object name will be the object name
    template_name = 'base/task_delete.html'
    success_url = reverse_lazy('tasks')
    pass


'''
listview look for mode.html in template  -> ModelName_list.html
DetailView -> ModelName_details.html
CreateView -> ModelName_form.html
createview gives us autoform to work with
reverse -> it redirect the page when click on submit
UpdateView -> ModelName_form.html
DeleteView -> ModelName_confirm_delete.html


what is middleware ?
we use mixins to ristrict the user
    LoginRequiredMixin -> we can restrict user as admin , user or many other role


Request URL:	http://127.0.0.1:8000/accounts/login/?next=/
todo_list -> setting
'''
