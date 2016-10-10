from django.shortcuts import render, redirect

from board.models import Post, Board, Comment


def new_post(request):
    board = Board.objects.get(id=request.GET['board'])
    return render(request, 'new_post.html', {'board': board})


def post_list(request, board_id):
    if request.method == 'POST':
        board = Board.objects.get(id=board_id)
        Post.objects.create(board=board, title=request.POST['post_title_text'], content=request.POST['post_content_text'])
        return redirect('/board/'+str(board_id))

    posts = Post.objects.all()

    return render(request, 'post_list.html', {'posts': posts, 'board_id': board_id})


def view_post(request, post_id):
    post = Post.objects.get(id=post_id)

    return render(request, 'view_post.html', {'post': post, 'board_id': post.board.id})


def board_list(request):
    board_count = Board.objects.all().count()
    if board_count == 0:
        Board.objects.create(name='Default')

    boards = Board.objects.all()

    return render(request, 'board_list.html', {'boards': boards})


def new_comment(request):
    if request.method == 'POST':
        post = Post.objects.get(id=request.POST['post_id'])
        Comment.objects.create(post=post, content=request.POST['comment_content'])
        return redirect(post)
