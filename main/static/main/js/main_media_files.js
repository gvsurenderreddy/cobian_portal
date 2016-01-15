$(document).ready(function() {
    $("select").change(function(){
        this.form.submit();
    });
});