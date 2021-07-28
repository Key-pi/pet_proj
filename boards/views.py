import csv

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView

from weasyprint import HTML

# from django.contrib import messages

from .forms import BoardForm, NewTopicForm, PostForm
from .models import Board, Post, Topic


class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'
    paginate_by = 20
    queryset = Board.objects.filter(is_active=True)


def save_board_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            board = Board.objects.all()
            data['html_partial_board'] = render_to_string('includes/partial_board.html', {
                'boards': board,
                'user': request.user
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def board_create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
    else:
        form = BoardForm()
    return save_board_form(request, form, 'board_create.html')


def board_update(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == "POST":
        form = BoardForm(request.POST, instance=board)
    else:
        form = BoardForm(instance=board)
    return save_board_form(request, form, 'board_update.html')


def board_delete(request, pk):
    board = get_object_or_404(Board, pk=pk)
    data = dict()
    boards = Board.objects.all()
    if request.method == 'POST':
        board.delete()
        data['form_is_valid'] = True
        data['html_partial_board'] = render_to_string('includes/partial_board.html', {
            'boards': boards,
            'user': request.user
        })
    else:
        context = {'boards': board}
        data['html_form'] = render_to_string('board_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_update').annotate(replies=Count('posts') - 1)
        return queryset


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('boards:topic_posts', pk=pk, topic_pk=topic.pk)
        else:
            return render(request, 'new_topic.html', {'form': form, 'board': board})

    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'form': form, 'board': board})


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_update = timezone.now()
            topic.save()

            topic_url = reverse('boards:topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
        else:
            return render(request, 'reply_topic.html', {'topic': topic, 'form': form})
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.update_by = self.request.user
        post.update_at = timezone.now()
        post.save()
        return redirect('boards:topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


def export_topic_csv(request, pk, topic_pk):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="topic.csv"'

    writer = csv.writer(response)
    writer.writerow(['Author', 'Message', 'Date'])

    posts = Post.objects.filter(topic=Topic.objects.get(pk=topic_pk)).values_list('topic', 'message', 'created_at')

    for post in posts:
        writer.writerow(post)

    return response


def export_topic_pdf(request, pk, topic_pk):
    topic = Topic.objects.get(pk=topic_pk)
    posts = Post.objects.filter(topic=topic)
    board = topic.board
    html_string = render_to_string(
        'topic_posts_to_pdf.html', {'posts': posts, 'topic': topic, 'board': board})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf')

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response
