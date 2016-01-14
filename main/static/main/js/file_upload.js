$(document).ready(function() {
    $("#submit_button").click(function() {
		$("#modal_uploading").modal({backdrop: "static"});
		$("#file_upload_form").submit();
    });
});