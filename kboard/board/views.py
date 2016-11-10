from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST, require_GET
from django.db.models import F
from django.conf import settings

from board.models import Post, Board, Comment, EditedPostHistory
from board.forms import PostForm
from core.utils import get_pages_nav_info


def handle_uploaded_file(f):
    with open(settings.BASE_DIR + '/file/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def home(request):
    return render(request, 'home.html')


def new_post(request, board_slug):
    board = Board.objects.get(slug=board_slug)
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.board = board
            post.save()
            return redirect(board)
    else:
        post_form = PostForm()

    return render(request, 'new_post.html', {'board': board, 'post_form': post_form})


def post_list(request, board_slug):
    board = Board.objects.get(slug=board_slug)

    # search
    search_info = {
        'query': request.GET.get('query', ''),
        'selected_flag': request.GET.get('search_flag', 'TITLE'),
        'flags': Post.SEARCH_FLAG
    }

    if search_info['query']:
        posts = Post.objects.board(board).remain().search(search_info['selected_flag'], search_info['query'])\
            .order_by('-id')
    else:
        posts = Post.objects.board(board).remain().order_by('-id')

    # pagination
    paginator = Paginator(posts, 10)  # Show 10 contacts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    pages_nav_info = get_pages_nav_info(posts, nav_chunk_size=10)

    return render(request, 'post_list.html', {
        'posts': posts,
        'board': board,
        'pages_nav_info': pages_nav_info,
        'search_info': search_info
    })


def view_post(request, post_id):
    non_sliced_query_set = Post.objects.filter(id=post_id)
    non_sliced_query_set.update(page_view_count=F('page_view_count') + 1)

    post = Post.objects.get(id=post_id)
    comments_all_list = Comment.objects.filter(post=post, is_deleted=False).order_by('-id')

    is_modified = False
    if post.created_time != post.modified_time:
        is_modified = True

    paginator = Paginator(comments_all_list, 5)  # Show 5 contacts per page
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comments = paginator.page(paginator.num_pages)

    pages_nav_info = get_pages_nav_info(comments, nav_chunk_size=10)

    return render(request, 'view_post.html', {
        'post': post,
        'is_modified': is_modified,
        'comments': comments,
        'pages_nav_info': pages_nav_info
    })


@require_GET
def post_history_list(request, post_id):
    post = Post.objects.get(id=post_id)
    post_history = EditedPostHistory.objects.filter(post=post).order_by('-id')

    return render(request, 'post_history_list.html', {
        'history_list': post_history,
        'post_id': post_id
    })


def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    origin_post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        if post.title != request.POST['title'] or post.content != request.POST['content'] or post.file.name != request.FILES.get('file', ''):
            if post_form.is_valid():
                edited_post_history = EditedPostHistory.objects.create(
                    post=origin_post,
                    title=origin_post.title,
                    content=origin_post.content,
                    file=origin_post.file,
                )
                edited_post_history.save()

                post_form.save()
                return redirect(post)
        else:
            error_message = "변경 사항이 없습니다"
            return render(request, 'edit_post.html', {'post': post, 'post_form': post_form, 'error_alert': error_message})

    else:
        post_form = PostForm(initial={'title': post.title, 'content': post.content, 'file': post.file})
    return render(request, 'edit_post.html', {'post': post, 'post_form': post_form})


def board_list(request):
    board_count = Board.objects.all().count()
    if board_count == 0:
        Board.objects.create(name='Default', slug='default')

    boards = Board.objects.all()

    return render(request, 'board_list.html', {'boards': boards})


@require_POST
def new_comment(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        Comment.objects.create(post=post, content=request.POST['comment_content'])
        return redirect(post)


@require_POST
def delete_comment(request, post_id, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        comment.is_deleted = True
        comment.save()

        return redirect(comment.post)


@require_POST
def delete_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        post.is_deleted = True
        post.save(update_fields=['is_deleted'])

        return redirect(post.board)


@require_POST
def like_post(request, post_id):
    post = Post.objects.filter(id=post_id)
    post.update(like_count=F('like_count') + 1)

    return redirect(post[0])
