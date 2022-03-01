// Assign handlers immediately after making the request,
// and remember the jqxhr object for this request
var jqxhr = $.getJSON("https://api.mercadolibre.com/sites/MLM/search?sort=price_asc&price=2900.0-6000.0&condition=used&category=MLM9761", function() {
        console.log("success");
    })
    .done(function() {
        console.log("second success");
    })
    .fail(function() {
        console.log("error");
    })
    .always(function() {
        console.log("complete");
    });

// Perform other work here ...

// Set another completion function for the request above
jqxhr.always(function() {
    console.log("second complete");
});