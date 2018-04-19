$('#alert-modal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var modal = $(this);
    modal.find('#alert_id').val(button.data('alert-id'));
    modal.find('#asset').val(button.data('alert-symbol'));
    modal.find('#market').val(button.data('alert-market'));
    modal.find('#cond_option').val(button.data('alert-condition'));
    modal.find('#price').val(button.data('alert-price'));
    modal.find('#percent').val(button.data('alert-percent'));
    modal.find('#percent_duration').val(button.data('alert-percent_duration'));
    modal.find('#phone_number').val(button.data('alert-phone_number'));
    onAlertCondChange(button.data('alert-condition'));
});

function onAlertCondChange(cond_option) {
    var priceElem = $('#price');
    var priceLabel = $('label[for="price"]');
    var percentElem = $('#percent');
    var percentLabel = $('label[for="percent"]');
    var percentDurationElem = $('#percent_duration');
    var percentDurationLabel = $('label[for="percent_duration"]');
    if (cond_option == '1' || cond_option == '0') {
        priceElem.show();
        priceLabel.show();
        percentElem.hide();
        percentLabel.hide();
        percentDurationElem.hide();
        percentDurationLabel.hide();
    } else if (cond_option == '2' || cond_option == '3') {
        priceElem.hide();
        priceLabel.hide();
        percentElem.show();
        percentLabel.show();
        percentDurationElem.show();
        percentDurationLabel.show();
    } else {
        priceElem.hide();
        priceLabel.hide();
        percentElem.hide();
        percentLabel.hide();
        percentDurationElem.hide();
        percentDurationLabel.hide();
    }
}

$('#cond_option').on('change', function (event) {
    var cond_option = event.target.value;
    onAlertCondChange(cond_option);
});
onAlertCondChange($('#cond_option').val());
