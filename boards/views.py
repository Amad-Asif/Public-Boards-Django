# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import View
from django.urls import reverse_lazy
from django.utils import timezone

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.urls import reverse_lazy

'''
Django view: it’s just a function that receives 
an HttpRequest object and returns an HttpResponse.
'''

'''
def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html',{'boards': boards})
'''

'''
A Generic Class Based View for the Homepage
We are just grabbing all the boards from the database 
and listing it in the HTML:
'''
from django.views.generic import ListView 

class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'


'''
Board topics without paginator
def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    # Here we are using annotate to generate a new column on the fly
    # This New column will be accessabe using topics.replies 
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'topics.html', {'board': board, 'topics': topics})

    # try:
    #     board = Board.objects.get(pk=pk)
    # except Board.DoesNotExist:
    #     raise Http404
    # return render(request, 'topics.html', {'board': board})
'''

'''
Using a function based view with paginator

def board_topics(request,pk):
    board = get_object_or_404(Board, pk=pk)
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 20)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request, 'topics.html', {'board':board, 'topics':topics})
'''

'''
Using class based view for Paginator
'''
class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super(TopicListView,self).get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset
    
        


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    #user = User.objects.first()
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user)
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


""" Without using Django Forms """
# def new_topic(request, pk):
#     board = get_object_or_404(Board, pk=pk)

#     if request.method == "POST":
#         subject = request.POST['subject']
#         message = request.POST['message']

#         user = User.objects.first()

#         topic = Topic.objects.create(
#             subject=subject,
#             board=board,
#             starter=user)
#         post = Post.objects.create(
#             message = message,
#             topic = topic,
#             created_by = user)
#         return redirect('board_topics', pk=board.pk)
#     return render(request, 'new_topic.html', {'board': board})

""" Topic Posts as Fucntion Based View 
def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    return render(request, 'topic_posts.html', {'topic': topic})

"""

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super(PostListView,self).get_context_data(**kwargs)
    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


''' Class Based Views '''
from django.views.generic import View

class ContactList(View):
    def get(self,request):
        return HttpResponse("No Contacts Available")

# class NewPostView(View):
#     def post(self,request):
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('post_list')
#         return render(request, 'new_post.html', {'form':form})
    
#     def get(self, request):
#         form = PostForm()
#         return render(request, 'new_post.html', {'form':form})

''' Generic Class Based Views '''
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

"""
We can’t decorate the class directly with the @login_required decorator. 
We have to use the utility @method_decorator, and pass a decorator 
(or a list of decorators) and tell which method should be decorated.
"""

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def form_valid(self,form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


