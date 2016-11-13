from board.models import Board


def navbar(request):
    boards = Board.objects.all()
    return {
        'boards': boards
    }
