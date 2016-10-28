$(document).ready(function() {
    $(".remove-comment").click(function(){
        var form = $(this).find('form');
        form.submit();
    });
});