
$("#asset").combobox();


appMarkets = {{ app_markets_json|safe }};
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