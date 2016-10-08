from django.shortcuts import render, redirect
from board.models import Post


def new_post(request):
    return render(request, 'new_post.html')


def post_list(request):
    if request.method == 'POST':
        Post.objects.create(title=request.POST['post_title_text'], content=request.POST['post_content_text'])
        return redirect('/board')

    posts = Post.objects.all()

    return render(request, 'post_list.html', {'posts': posts})


def view_post(request, post_id):
    post_ = Post.objects.get(id = post_id)

    return render(request, 'view_post.html', {'post': post_})


def board_list(request):
    board_count = Board.objects.all().count()
    if board_count == 0:
        Board.objects.create(name='Default')

    boards = Board.objects.all()

    return render(request, 'board_list.html', {'boards': boards})
