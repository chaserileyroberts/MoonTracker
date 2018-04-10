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
        appMarkets = {{ app_markets_json|safe }};
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
