$(document).ready(function() {
    $(".remove-comment").click(function(){
        var form = $(this).find('form');
        form.submit();
    });
    
    $(".move-button").click(function(){
        var path = $(this).attr('path');
        location.href = path;
    });
});