$(document).ready(function() {

    //SCROLL EFECTO BARRA HERRAMIENTAS
    // When the user scrolls the page, execute myFunction
    window.onscroll = function() { myFunction() };
    var navbar = $('.herramientas')
    var container = $('.container')
    var agrupar = $('#agrupar')
    var posicion = 0;
    var posicionMax = 0;
    var delay = 500;

    var lista = $('#listas')

    $('a').click(function(event) {
        event.preventDefault();
    });

    // Get the offset position of the navbar
    var sticky = navbar.offset();
    // Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
    function myFunction() {
        if (window.pageYOffset >= sticky.top) {
            navbar.addClass("sticky")
        } else {
            navbar.removeClass("sticky");
        }
    }

    $.ajax({
        url: "https://api.mercadolibre.com/sites/MLM/search?sort=price_asc&price=2900.0-6000.0&condition=used&category=MLM9761",
        method: "GET",
        dataType: 'json',
        success: function(data) {
            var total = '';
            posicionMax = Math.ceil(data.paging.total / 50);
            //Agregar resultados totales a documento
            total += '<span>' + data.paging.total + ' resultados</span>';
            $('.total').append(total);
            for (i = 0; i <= posicionMax; i++) {
                $.ajax({
                    url: "https://api.mercadolibre.com/sites/MLM/search?sort=price_asc&price=2900.0-6000.0&condition=used&category=MLM9761&offset=" + (posicion + 50),
                    method: "GET",
                    dataType: 'json',
                    success: function(data) {
                        var base = '';
                        $.each(data.results, function(key, value) {
                            base +=
                                '<a href="' + value.permalink + '" target="_blank" class="linkML">' +
                                '<div class="contenedorProductos productosAgrupados">' +
                                '<img src="' + value.thumbnail + '"" alt="' + value.title + '"></img>' +
                                '<h3>' + value.title + '</h3>' +
                                '<div class="datosProductos">' +
                                '<span>$' + value.price + '</span>' +
                                '<span class="condicion">' + value.condition + '</span>' +
                                '<span class="envio">' + value.shipping.free_shipping + '</span>' +
                                '</div>' +
                                '</div>' +
                                '</a>';
                        });
                        $('.container').append(base);
                    },
                    error: function() {
                        console.log(data);
                    }
                }).done(function() {

                    //$('.contenedorProductos').each(function() {
                    //    console.log($(this))
                    //    ScrollReveal().reveal($(this), { delay: delay });
                    //    delay += 100;
                    //});

                    $(".condicion").each(function(i, obj) {
                        if ($(this).text("used")) {
                            $(this).text("Usado")
                        } else if ($(this).text("new")) {
                            $(this).text("Nuevo")
                        }
                    });
                    $(".envio").each(function(i, obj) {
                        if ($(this).text() == "true") {
                            $(this).text("Envio Gratis")
                            $(this).css("color", "green")
                        } else if ($(this).text() == "false") {
                            $(this).text("+Envio")
                            $(this).css("color", "red")
                        }
                    });

                });
            }

        },
        error: function() {
            console.log(data);
        }
    }).done(function() {

    });
    //--------------------------------------------------------


    //---------------------------------------------





    $(document).ready(function() {
        agrupar.click(function(event) {
            container.removeClass("lista");
            container.addClass("agrupado")
            $('.contenedorProductos').each(function() {
                $('.contenedorProductos').removeClass("productosListas");
                $('.contenedorProductos').addClass("productosAgrupados");
            });


        });
        lista.click(function(event) {
            container.removeClass("agrupado");
            container.addClass("lista")
            $('.contenedorProductos').each(function() {
                $('.contenedorProductos').removeClass("productosAgrupados");
                $('.contenedorProductos').addClass("productosListas")
            });

        });
        //GENERAR NUEVO CONTENIDO HASTA TERMINAR - EFECTO SCROLL INFINITO

    });
});