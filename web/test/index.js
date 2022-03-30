$(document).ready(function() {
    var posicion = 0;
    var posicionMax = 0;
    var guardar = []
    var options = []
    var difActual = []
    var difOld = []
    var actual = []
    var storedNames = JSON.parse(localStorage.getItem("values"));
    $('a').click(function(event) {
        event.preventDefault();
    });


    //console.log(storedNames)
    $.ajax({
        url: "https://api.mercadolibre.com/sites/MLM/search?sort=price_asc&price=2900.0-6000.0&condition=used&category=MLM9761",
        method: "GET",
        dataType: 'json',
        success: function(data) {
            var total = '';
            posicionMax = Math.ceil(data.paging.total / 50);
            loadContent(data, '.productos')
                //Agregar resultados totales a documento
            total += '<span>' + data.paging.total + ' resultados</span>';
            $('.total').append(total);
            for (i = 0; i <= posicionMax; i++) {
                $.ajax({
                    url: "https://api.mercadolibre.com/sites/MLM/search?sort=price_asc&price=2900.0-6000.0&condition=used&category=MLM9761&offset=" + (posicion += 50),
                    method: "GET",
                    dataType: 'json',
                    success: function(data) {
                        loadContent(data, '.productos')
                    },
                    error: function() {
                        console.log(data);
                    }
                }).done(function() {
                    zoom();
                    changeText();
                });
            }

        },
        error: function() {
            console.log(data);
        }
    }).done(function() {
        zoom();
        changeText();
        $('#save').click(function(e) {
            //$.each(guardar, function(index, value) {
            //    $.each(value, function(producto, values) {
            //        options.push(value[producto])
            //    });
            //});
            //localStorage.setItem("values", JSON.stringify(options));
            Swal.fire(
                'Guardada con éxito',
                'Ahora puedes esperar a que publiquen gráficas',
                'success'
            )
        });
        $('#compare').click(function(e) {
            cambios();
        });

        $('#reset').click(function(e) {
            Swal.fire({
                title: '¿Estas segur@?',
                text: "Esto vaciará la lista guardada que tengas!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Continuar'
            }).then((result) => {
                if (result.isConfirmed) {
                    //localStorage.clear();
                    Swal.fire(
                        '¡Eliminado!',
                        'Puedes guardar alguna nueva lista cuando desees',
                        'success'
                    )
                }
            })

        });

        $('#download').click(function(e) {
            saver(storedNames, 'Lista')
        });
    });


    function loadContent(data, select) {
        var base = '';
        if (select == '.nuevos' || select == '.vendidas') {
            str = data.title;
            base +=
                '<tr>' +
                '<td id="img-tabla">' + '<div class="img-content">' + '<img src="' + data.thumbnail.replace("I.jpg", "F.jpg") + '" alt="' + data.title + '">' + '</div>' + '</td>' +
                '<td>' + '<a href="' + data.permalink + '" target="_blank">' + $.trim(str) + '</a>' + '</td>' +
                '<td class="center">$' + data.price + '</td>' +
                '<td class="status center">' + data.shipping.free_shipping + '</td>' +
                '</tr>';
            $(select).append(base);
            return false;
        }
        guardar.push(data.results)

        $.each(data.results, function(key, value) {
            str = value.title;
            base +=
                '<tr>' +
                '<td id="img-tabla">' + '<div class="img-content">' + '<img src="' + value.thumbnail.replace("I.jpg", "F.jpg") + '" alt="' + value.title + '">' + '</div>' + '</td>' +
                '<td>' + '<a href="' + value.permalink + '" target="_blank">' + $.trim(str) + '</a>' + '</td>' +
                '<td class="center">$' + value.price + '</td>' +
                '<td class="status center">' + value.shipping.free_shipping + '</td>' +
                '</tr>'
        });
        $(select).append(base);
    }

    //loadContent(data ,'.container');
    function cambios() {
        $.each(guardar, function(arreglos, data) {
            $.each(data, function(producto, values) {
                actual.push(data[producto])
            });
        });


        for (var i = 0; i <= actual.length; i++) {
            if (!storedNames.some(item => item.id === actual[i].id)) {
                loadContent(actual[i], '.nuevos')
            }
            if (storedNames[i] === undefined) {
                return false;
            }
            if (!actual.some(item => item.id === storedNames[i].id)) {
                loadContent(storedNames[i], '.vendidas')
            }
            zoom();
            changeText()
        }
        //$.each(difActual, function(i, data) {
        //$.each(difActual, function(i, data) {
        //    if (!difOld.some(item => item === difActual[i])) {
        //        //loadContent(difActual[i], '.nuevos')
        //        console.log(difActual[i].id)
        //    }
        //    if (!difActual.some(item => item.id === difOld[i].id)) {
        //        console.log(difOld[i])
        //        loadContent(difOld[i], '.vendidas')
        //    }
        //});


        //saver(difActual, 'difActual')
        //saver(difOld, 'difOld')
    };

    function saver(texto, nombre) {
        const textToBLOB = new Blob([JSON.stringify(texto, null, 2)], { type: 'text/plain' });
        const sFileName = nombre + '.txt'; // The file to save the data.

        let newLink = document.createElement("a");
        newLink.download = sFileName;

        if (window.webkitURL != null) {
            newLink.href = window.webkitURL.createObjectURL(textToBLOB);
        } else {
            newLink.href = window.URL.createObjectURL(textToBLOB);
            newLink.style.display = "none";
            document.body.appendChild(newLink);
        }
        newLink.click();
    }


    function nuevos() {

    };

    function zoom() {
        $('#img-tabla img').each(function(i) {
            $(this).click(function(e) {
                $('.img-open-background').css("visibility", "visible");
                $(this).addClass('imgclick');
                e.stopPropagation();
            });
            $('.img-open-background').click(function() {
                $('.imgclick').removeClass('imgclick');
                $('.img-open-background').css("visibility", "hidden");
            });
            $(document).on('keydown', function(event) {
                $('.imgclick').removeClass('imgclick');
                $('.img-open-background').css("visibility", "hidden");
            });
        });
    }

    function changeText(content) {
        var self = $(this);
        $(".condicion").each(function(i, obj) {
            if ($(this).text("used")) {
                $(this).text("Usado")
            } else if ($(this).text("new")) {
                $(this).text("Nuevo")
            }
        });
        $(".status").each(function(i, obj) {
            if ($(this).text() == "true") {
                $(this).text("Envio")
                $(this).css("color", "green")
            } else if ($(this).text() == "false") {
                $(this).text("+Envio")
                $(this).css("color", "red")
            }
        });
    }
    //    $(".condicion").each(function(i, obj) {
    //        if ($(this).text("used")) {
    //            $(this).text("Usado")
    //        } else if ($(this).text("new")) {
    //            $(this).text("Nuevo")
    //        }
    //    });
    //    $(".status").each(function(i, obj) {
    //        if ($(this).text() == "true") {
    //            $(this).text("Envio")
    //            $(this).css("color", "green")
    //        } else if ($(this).text() == "false") {
    //            $(this).text("+Envio")
    //            $(this).css("color", "red")
    //        }
    //    });
    //}

    $('th').click(function() {
        var table = $(this).parents('table').eq(0)
        var rows = table.find('tr:gt(0)').toArray().sort(comparer($(this).index()))
        this.asc = !this.asc
        if (!this.asc) {
            rows = rows.reverse()
        }
        for (var i = 0; i < rows.length; i++) {
            table.append(rows[i])
        }
    })

    function comparer(index) {
        return function(a, b) {
            var valA = getCellValue(a, index),
                valB = getCellValue(b, index)
            return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.toString().localeCompare(valB)
        }
    }

    function getCellValue(row, index) {
        return $(row).children('td').eq(index).text()
    }


    $('.search').each(function() {
        var self = $(this);
        var div = self.children('div');
        var placeholder = div.children('input').attr('placeholder');
        var placeholderArr = placeholder.split(/ +/);
        if (placeholderArr.length) {
            var spans = $('<div />');
            $.each(placeholderArr, function(index, value) {
                spans.append($('<span />').html(value + '&nbsp;'));
            });
            div.append(spans);
        }
        self.click(function() {
            self.addClass('open');
            setTimeout(function() {
                self.find('input').focus();
            }, 750);
        });
        $(document).click(function(e) {
            if (!$(e.target).is(self) && !jQuery.contains(self[0], e.target)) {
                self.removeClass('open');
            }
        });
    });
    $('#reload').click(function() {
        $('html,body').animate({
            scrollTop: $('html').offset().top
        }, 'slow');
    });

});