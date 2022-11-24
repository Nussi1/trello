import json
from pydoc import browse

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView
)

from .forms import CommentForm, UploadFieldForm
from .models import Entry, Column, Comment, Window

from django.db.models import Case, Count, BooleanField, When, F


class WindowView(ListView):
  template_name = 'board/window.html'
  model = Window
  queryset = Window.objects.all()


class WindowDetailView(DetailView):
  model = Window
  template_name = 'index.html'

  def get_context_data(self, **kwargs):
    pk = self.kwargs.get('pk')
    desk = Window.objects.get(id=pk)
    columns = Column.objects.filter(window=desk)

    context = {
      'columns': columns, 'window': desk}
    return context


def Windows(request):
  title = "All Boards"
  boards = Window.objects.annotate(
    favourited_by_user=Count(Case(
      When(is_favourite=request.user, then=1), output_field=BooleanField(),)),).order_by('-id')
  my_boards = Window.objects.filter(user=request.user).order_by('-id')
  context = {"boards": boards, "my_boards": my_boards, "title": title}
  return render(request, 'board/window.html', context)



def favourite_list(request):
  user = request.user
  favourite_windows = user.favourite.all()
  context = {
    'favourite_windows': favourite_windows,
  }
  return render(request, 'board/favourites.html', context)



def favourite_add(request, id):
  desk = get_object_or_404(Window, id=id)
  if request.method == "POST":
    if desk.favourite.filter(id=request.user.id).exists():
      desk.favourite.remove(request.user)
    else:
      desk.favourite.add(request.user)
  return redirect('window')


#---------------Archive----------------

def Archives(request):
  title = "All Archived Desks"
  boards = Window.objects.annotate(
    archived_by_user=Count(Case(
      When(is_archived=request.user, then=1), output_field=BooleanField(),)),).order_by('-id')
  my_boards = Window.objects.filter(user=request.user).order_by('-id')
  context = {"boards": boards, "my_boards": my_boards, "title": title}
  return render(request, 'board/window.html', context)



def archived_list(request):
  user = request.user
  archived_windows = user.archive.all()
  context = {
    'archived_windows': archived_windows,
  }
  return render(request, 'board/archived.html', context)



def add_to_archive(request, id):
  desk = get_object_or_404(Window, id=id)
  if request.method == "POST":
    if desk.archive.filter(id=request.user.id).exists():
      desk.archive.remove(request.user)
    else:
      desk.archive.add(request.user)
  return redirect('window')







#-----------------Cards--------------

class IndexView(ListView):
    template_name = 'index.html'
    model = Entry

    def get_context_data(self, **kwargs):
        # boards = Entry.objects.all()
        context = super().get_context_data(**kwargs)
        context = {
          "entry-list": self.model.objects.all(),
        }
        return context


class LockedView(LoginRequiredMixin):
    login_url = "admin:login"


class EntryListView(LockedView, ListView):
    template_name = 'index.html'
    model = Entry
    queryset = Column.objects.all()


class EntryDetailView(LockedView, DetailView):
    model = Entry


class EntryCreateView(LockedView, SuccessMessageMixin, CreateView):
    model = Entry
    fields = '__all__'
    # success_url = reverse_lazy("entry-list")
    queryset = Entry.objects.all()
    success_message = "Your new entry was created!"

    def get_success_url(self):
      return reverse_lazy('detail-view', kwargs={'pk': self.object.column.window.pk})


class EntryUpdateView(LockedView, SuccessMessageMixin, UpdateView):
    model = Entry
    fields = '__all__'
    success_message = "Your entry was updated!"
    # success_url = reverse_lazy("entry-list")

    def get_success_url(self):
      return reverse_lazy('detail-view', kwargs={'pk': self.object.column.window.pk})


class EntryDeleteView(LockedView, SuccessMessageMixin, DeleteView):
    model = Entry
    success_url = reverse_lazy("entry-list")
    success_message = "Your entry was deleted!"

    def get_success_url(self):
      return reverse_lazy('detail-view', kwargs={'pk': self.object.column.window.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

#--------------------Column------------------



class ColumnIndexView(ListView):
  model = Column
  template_name = 'index.html'
  queryset = Window.objects.all()




class ColumnDetailView(DetailView):
  model = Column
  template_name = 'index.html'

  def get_context_data(self, **kwargs):
    pk = self.kwargs.get('pk')
    column = Column.objects.get(id=pk)
    entries = Entry.objects.filter(column=column)

    context = {
      'entries': entries, 'column': column}
    return context


class ColumnCreateView(CreateView):
  model = Column
  fields = '__all__'
  # success_url = reverse_lazy("entry-list")
  queryset = Column.objects.all()

  def get_success_url(self):
    return reverse_lazy('detail-view', kwargs={'pk': self.object.window.pk})


class ColumnUpdateView(UpdateView):
  model = Column
  fields = '__all__'
  template_name_suffix = '_update_form'
  # success_url = reverse_lazy("detail-view")

  def get_success_url(self):
    return reverse_lazy('detail-view', kwargs={'pk': self.object.window.pk})


class ColumnDeleteView(DeleteView):
  model = Column
  # success_url = reverse_lazy('detail-view')

  def get_success_url(self):
    return reverse_lazy('detail-view', kwargs={'pk': self.object.window.pk})



class CardDetailView(FormView, DetailView):
  template_name = "board/view_detail.html"
  model = Entry
  context_object_name = 'entry'
  form_class = CommentForm
  success_url = "#"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['comments'] = Comment.objects.filter(entry=self.get_object()).order_by('-created_on')
    context['form'] = CommentForm()
    return context

  def post(self, request, *args, **kwargs):
    if self.request.method == 'POST':
      form = CommentForm(self.request.POST)
      if form.is_valid():
        comment = Comment(
          author=self.request.user,
          body=form.cleaned_data["body"],
          entry=self.get_object(),
        )
        comment.save()

      return super().form_valid(form)


class FileListView(ListView):
  queryset = Entry.objects.all()
  template_name = 'board/view_detail.html'

  def get_queryset(self):
    return Entry.objects.all()





