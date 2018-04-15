$('#alert-modal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var modal = $(this);
    modal.find('#alert_id').val(button.data('alert-id'));
    modal.find('#asset').val(button.data('alert-symbol'));
    modal.find('#less_more').val(button.data('alert-above'));
    modal.find('#target_price').val(button.data('alert-price'));
    modal.find('#phone_number').val(button.data('alert-phone-number'));
});
