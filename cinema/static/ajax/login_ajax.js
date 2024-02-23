$(document).ready(function () {
    $('#form_ajax').submit(function (e) {
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: this.action,
            data: $(this).serialize(),
            dataType: 'json',
            success: function (response) {
                if (response.success) {
                    window.location.replace('{% url "cinema:index" %}');
                    // пауза
                    $('.modal-content').html(response.html);
                    $('#login_ajax').modal('show');
                } else if (response.error) {
                    console.log(response.error)
                    $('.alert-danger').text(response.error).removeClass('d-none');
                }
            },
            error: function (xhr, textStatus, errorThrown) {
                console.log('Error:', textStatus, errorThrown);
            }
        });
    });
})
