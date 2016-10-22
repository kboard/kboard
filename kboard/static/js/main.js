$(document).ready(function() {
    $(".remove-comment").click(function(){
        var comment_id = $(this).attr('comment-id');
        var form = $('#comment_delete_form');

        form.find('input[name="comment_id"]').val(comment_id);
        form.submit();
    })
});