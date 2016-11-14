$(document).ready(function() {
    $(".delete-comment").click(function(){
        var form = $(this).parent().find('form');
        form.submit();
    });
    
    $(".redirection-button").click(function(){
        var path = $(this).attr('path');
        location.href = path;
    });

    $('.comment-iframe').on('load', function () {
        var height = this.contentWindow.document.body.offsetHeight;
        $(this).height(height);
    });

    $('#id_content_iframe').on('load', function () {
        var height = this.contentWindow.document.body.offsetHeight;
        $(this).height(height);
        $(this).attr('scrolling', 'no');
    });

    $('.post-submit-button').click(function () {
        var title = $('#id_post_title').val();
        var contentHTML = $('#id_content').val();
        var content = $('<div>' + contentHTML + '</div>').text();

        if(title.trim() && content.trim()){
            $('.post-form').submit();
        }else{
            alert("제목과 내용을 채워주세요!" + content);
        }
    });
});
