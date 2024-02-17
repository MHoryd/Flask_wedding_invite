$(document).ready(function () {
    $("#submitBtn").click(function (event) {
        event.preventDefault();

        $("#loadingSpinner").show();

        $.ajax({
            type: "POST",
            url: $("#myForm").attr("action"),
            data: $("#myForm").serialize(),
            success: function (response) {
                $("#loadingSpinner").hide();

                if (response.success) {
                    $("#flashMessage").html(response.message).css("color", "green").show();
                } else {
                    $("#flashMessage").html(response.message).css("color", "red").show();
                }
            },
            error: function (xhr) {
                $("#loadingSpinner").hide();

                if (xhr.status == 429) {
                    $('#flashMessage').html('Za dużo prób, spróbuj za mnutę.').css("color", "red").show();
                } else {
                    $('#flashMessage').html('Wystąpił błąd którego nie oczekiwałem. Najlepiej napisz do nas na messengerze ;)').css("color", "red").show();
                }
            }
        });
    });
});