from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST, require_GET
from django.core.urlresolvers import reverse
from django.db.models import F
from django.conf import settings

from board.models import Post, Board, Comment, EditedPostHistory, Attachment
from board.forms import PostForm, AttachmentForm
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
        attachment_form = AttachmentForm(request.POST, request.FILES)
        if post_form.is_valid() and attachment_form.is_valid():
            post = post_form.save(commit=False)
            post.board = board
            post.save()
            attachment = attachment_form.save(commit=False)
            attachment.post = post
            attachment.save()
            return redirect(board)
    else:
        post_form = PostForm()
        attachment_form = AttachmentForm()

    return render(request, 'new_post.html', {'board': board, 'post_form': post_form, 'attachment_form': attachment_form})


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
    paginator = Paginator(posts, board.posts_chunk_size)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    pages_nav_info = get_pages_nav_info(posts, nav_chunk_size=board.post_pages_nav_chunk_size)

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
    history = EditedPostHistory.objects.filter(post=post)
    if history:
        is_modified = True

    paginator = Paginator(comments_all_list, post.board.comments_chunk_size)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comments = paginator.page(paginator.num_pages)

    pages_nav_info = get_pages_nav_info(comments, nav_chunk_size=post.board.comment_pages_nav_chunk_size)

    return render(request, 'view_post.html', {
        'post': post,
        'is_modified': is_modified,
        'comments': comments,
        'pages_nav_info': pages_nav_info
    })


def comment_list(request, post_id):
    post = Post.objects.get(id=post_id)
    comments_all_list = Comment.objects.filter(post=post, is_deleted=False).order_by('-id')

    paginator = Paginator(comments_all_list, post.board.comments_chunk_size)
    page = request.GET.get('page')

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comments = paginator.page(paginator.num_pages)

    pages_nav_info = get_pages_nav_info(comments, nav_chunk_size=post.board.comment_pages_nav_chunk_size)

    return render(request, 'comment_list.html', {
        'post': post,
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
    try:
        attachment = Attachment.objects.get(post=post)
        attachment_name = attachment.attachment.name
    except Attachment.DoesNotExist:
        attachment = None
        attachment_name = ''

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        attachment_form = AttachmentForm(request.POST, request.FILES, instance=attachment)
        if post.title != request.POST['title'] or post.content != request.POST['content'] or \
                attachment_name != request.FILES.get('attachment', ''):
            if post_form.is_valid() and attachment_form.is_valid():
                edited_post_history = EditedPostHistory.objects.create(
                    post=origin_post,
                    title=origin_post.title,
                    content=origin_post.content,
                    file=origin_post.file,
                )
                edited_post_history.save()

                post.save()

                attachment = attachment_form.save(commit=False)
                attachment.post = post
                attachment.save()
                return redirect(post)
        else:
            error_message = "변경 사항이 없습니다"
            return render(request, 'edit_post.html', {
                'post': post,
                'post_form': post_form,
                'attachment_form': attachment_form,
                'error_alert': error_message
            })
    else:
        post_form = PostForm(initial={'title': post.title, 'content': post.content, 'file': post.file})
        if attachment:
            attachment_form = AttachmentForm(initial={'attachment': attachment.attachment})
        else:
            attachment_form = AttachmentForm()

    return render(request, 'edit_post.html', {'post': post, 'post_form': post_form, 'attachment_form': attachment_form})


def board_list(request):
    boards = Board.objects.all()

    return render(request, 'board_list.html', {'boards': boards})


@require_POST
def new_comment(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        Comment.objects.create(post=post, content=request.POST['comment_content'])
        return redirect(reverse('board:comment_list', args=[post_id]))


@require_POST
def delete_comment(request, post_id, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        comment.is_deleted = True
        comment.save()

        return redirect(reverse('board:comment_list', args=[post_id]))


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
