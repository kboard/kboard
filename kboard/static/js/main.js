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
});
