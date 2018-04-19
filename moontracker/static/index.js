$.widget("custom.combobox", {
    _create: function() {
        this.wrapper = $("<span>")
            .addClass("custom-combobox")
            .insertAfter(this.element);
        this.element.val("");
        var marketElem = $('#market');
        marketElem.val('');
        this.element.hide();
        this._createAutocomplete();
    },

    _createAutocomplete: function() {
        var selected = this.element.children(":selected"),
            value = selected.val() ? selected.text() : "";

        this.input = $("<input>")
            .appendTo(this.wrapper)
            .val(value)
            .attr("title", "")
            .addClass("custom-combobox-input form-control")
            .autocomplete({
                delay: 0,
                minLength: 0,
                source: $.proxy(this, "_source")
            })
            .tooltip();

        this._on(this.input, {
            autocompleteselect: function(event, ui) {
                var marketElem = $('#market');
                marketElem.val('')
                ui.item.option.selected = true;
                this._trigger("select", event, {
                    item: ui.item.option
                });
            },

            autocompletechange: "_removeIfInvalid"
        });
    },

    _source: function(request, response) {
        var matcher = new RegExp($.ui.autocomplete.escapeRegex(request.term), "i");
        response(this.element.children("option").map(function() {
            var text = $(this).text();
            if (this.value && (!request.term || matcher.test(text)))
                return {
                    label: text,
                    value: text,
                    option: this
                };
        }));
    },

    _removeIfInvalid: function(event, ui) {
        // Search for a match (case-insensitive)

        var product = "";
        var value = this.input.val(),
            valueLowerCase = value.toLowerCase(),
            valid = false;
        
        var marketElem = $('#market');
        marketElem.val('')
        this.element.children("option").each(function() {
            if ($(this).text().toLowerCase() === valueLowerCase) {
                product = $(this).val();
                this.selected = valid = true;
                return false;
            }
        });
        // Found a match, nothing to do
        if (valid) {
            marketElem.prop('disabled', false);
            marketElem.empty();
            marketElem.append($("<option />").val('').text(''));
            $.each(appMarkets[product].markets, function (index, market) {
                marketElem.append($("<option />").val(market).text(market));
            });
            return;
        }
        // Disable if not valid
        marketElem.empty();
        marketElem.prop('disabled', true);
        // Remove invalid value
        this.input
            .val("")
            .attr("title", value + " didn't match any item")
            .tooltip("open");
        this.element.val("");
        this._delay(function() {
            this.input.tooltip("close").attr("title", "");
        }, 2500);
        this.input.autocomplete("instance").term = "";
    },

    _destroy: function() {
        this.wrapper.remove();
        this.element.show();
    }
});
$("#asset").combobox();

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

var lplSocket = io('/lastpriceslive', { transports: ['websocket'] });
lplSocket.on('json', function (lastPricesStr) {
    var lastPricesTableElem = $('#last-prices-table');
    if (lastPricesTableElem.length == 0) {
        var lastPricesElem = $('#last-prices');
        lastPricesElem.append($('<h4>').text('Last Prices'));
        var tableCElem = $('<div id="last-prices-table" class="table">');
        var headerCElem = $('<div class="table-header table-row">');
        headerCElem.append($('<div class="table-col last-prices-col-0-2">').text('Coin'));
        headerCElem.append($('<div class="table-col last-prices-col-1-2">').text('Price'));
        tableCElem.append(headerCElem);
        lastPricesElem.append(tableCElem);
        lastPricesTableElem = lastPricesElem.find('#last-prices-table');
    }

    var lastPrices = JSON.parse(lastPricesStr);
    $.each(lastPrices, function (index, lastPrice) {
        var symbolText = appMarkets[lastPrice.symbol]['name'];
        var rowFound = false;
        lastPricesTableElem.find('.table-row').each(function (index, rowElem) {
            var rowSymbol = $(rowElem).find('.last-prices-col-symbol').text();
            if (rowSymbol == symbolText) {
                var rowPriceElem = $(rowElem).find('.last-prices-col-price');
                var oldPriceText = rowPriceElem.text();
                rowPriceElem.text('$' + lastPrice.price);
                if (rowPriceElem.text() !== oldPriceText) {
                    rowPriceElem.addClass('last-prices-flash-update', 0);
                    rowPriceElem.removeClass('last-prices-flash-update', 800);
                }
                rowFound = true;
                return false;
            }
        });
        if (!rowFound) {
            var rowCElem = $('<div class="table-row">');
            var symbolText = appMarkets[lastPrice.symbol]['name'];
            rowCElem.append($('<div class="table-col last-prices-col-0-2 last-prices-col-symbol">').text(symbolText));
            var priceText = '$' + lastPrice.price;
            rowCElem.append($('<div class="table-col last-prices-col-1-2 last-prices-col-price">').text(priceText));
            lastPricesTableElem.append(rowCElem);
        }
    });
});




// make this work for appDurations
$.widget("custom.combobox", {
    _create: function() {
        this.wrapper = $("<span>")
            .addClass("custom-combobox")
            .insertAfter(this.element);
        this.element.val("");
        var durationElem = $('#duration');
        durationElem.val('');
        this.element.hide();
        this._createAutocomplete();
    },

    _createAutocomplete: function() {
        var selected = this.element.children(":selected"),
            value = selected.val() ? selected.text() : "";

        this.input = $("<input>")
            .appendTo(this.wrapper)
            .val(value)
            .attr("title", "")
            .addClass("custom-combobox-input form-control")
            .autocomplete({
                delay: 0,
                minLength: 0,
                source: $.proxy(this, "_source")
            })
            .tooltip();

        this._on(this.input, {
            autocompleteselect: function(event, ui) {
                var durationElem = $('#duration');
                durationElem.val('')
                ui.item.option.selected = true;
                this._trigger("select", event, {
                    item: ui.item.option
                });
            },

            autocompletechange: "_removeIfInvalid"
        });
    },

    _source: function(request, response) {
        var matcher = new RegExp($.ui.autocomplete.escapeRegex(request.term), "i");
        response(this.element.children("option").map(function() {
            var text = $(this).text();
            if (this.value && (!request.term || matcher.test(text)))
                return {
                    label: text,
                    value: text,
                    option: this
                };
        }));
    },

    _removeIfInvalid: function(event, ui) {
        // Search for a match (case-insensitive)

        var market = "";
        var value = this.input.val(),
            valueLowerCase = value.toLowerCase(),
            valid = false;
        
        var durationElem = $('#duration');
        durationElem.val('')
        this.element.children("option").each(function() {
            if ($(this).text().toLowerCase() === valueLowerCase) {
                market = $(this).val();
                this.selected = valid = true;
                return false;
            }
        });
        // Found a match, nothing to do
        if (valid) {
            durationElem.prop('disabled', false);
            durationElem.empty();
            durationElem.append($("<option />").val('').text(''));
            $.each(appDurations[market], function (index, duration) {
                durationElem.append($("<option />").val(duration).text(duration));
            });
            return;
        }
        // Disable if not valid
        durationElem.empty();
        durationElem.prop('disabled', true);
        // Remove invalid value
        this.input
            .val("")
            .attr("title", value + " didn't match any item")
            .tooltip("open");
        this.element.val("");
        this._delay(function() {
            this.input.tooltip("close").attr("title", "");
        }, 2500);
        this.input.autocomplete("instance").term = "";
    },

    _destroy: function() {
        this.wrapper.remove();
        this.element.show();
    }
});
$("#market").combobox();