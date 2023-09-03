from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from pet_owners.utils import DataMixin
from pet_owners.models import OwnerPost, PostComment, Owner
from .forms import *


class CreateComment(LoginRequiredMixin, DataMixin, CreateView):
    """Страница создания комментария"""
    form_class = AddOrEditCommentForm
    template_name = 'comments/add_comment_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление комментария"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = OwnerPost.objects.get(pk=self.kwargs['post_id'])
        form.save()
        return redirect('post', post_id=self.kwargs['post_id'])


class UpdateComment(LoginRequiredMixin, DataMixin, UpdateView):
    """Страница редактирования комментария"""
    form_class = AddOrEditCommentForm
    template_name = 'comments/edit_comment_page.html'

    def get_queryset(self):
        return PostComment.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактирование комментария"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context

    def form_valid(self, form):
        if 'update' in self.request.POST:
            form.save()
        return redirect('post', post_id=self.kwargs['post_id'])


class DeleteComment(LoginRequiredMixin, DataMixin, DeleteView):
    """Страница удаления комментария"""
    model = PostComment
    template_name = 'comments/delete_comment_page.html'

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'post_id': self.kwargs['post_id']})

    def get_queryset(self):
        qs = super(DeleteComment, self).get_queryset()
        return qs.filter(author=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Удаление комментария"
        context.update(self.get_left_menu())
        context.update(self.get_right_menu())
        return context


@login_required
def put_or_remove_like_for_comment(request, post_id, comment_id):
    """Ставит или убирает лайк комментарию"""
    user = Owner.objects.get(pk=request.user.id)
    comment = PostComment.objects.get(pk=comment_id)
    if user in comment.likes.all():
        comment.likes.remove(user)
    else:
        comment.likes.add(user)
    return redirect('post', post_id=post_id)