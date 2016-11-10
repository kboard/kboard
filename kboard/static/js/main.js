$(document).ready(function() {
    $(".remove-comment").click(function(){
        var form = $(this).find('form');
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
