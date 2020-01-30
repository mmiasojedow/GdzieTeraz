console.log('dziala');

let tables = $(".table");

tables.click(function () {
    console.log($(this).data('info'));
    let info = $(this).data('info');
    $(this).toggleClass('True');

    let checkbox = $(`[value=${info}]`);
    if ($(this).hasClass('True')) {
        checkbox.attr('checked', true);
    } else {
        checkbox.attr('checked', false);
    }
});

let reset = $('#reset');
reset.click(function () {
    tables.removeClass('True');
    let checkboxes = $('[type="checkbox"]');
    checkboxes.removeAttr('checked')

});

let restaurants = $('.rest-name');

restaurants.click(function () {
    let info = $(this).data('info');
    let hidden = $(this).find('.hidden_div');
    console.log(hidden);
    hidden.slideToggle();

    $.ajax({
        url: "api-restaurant/" + info,
    }).done(function (data) {
        let line1 = `<p>Wolne stoliki: ${data.free_tables}/${data.tables}</p>`;
        let line2 = `<p>Wolne miejsca: ${data.free_seats}/${data.seats}</p>`;
        let line3 = `<p>Kuchnia: ${data.kitchen}</p>`;
        let line4 = `<p>Adres: ${data.address}, ${data.city}</p>`;
        let line5 = `<p>Telefon: ${data.phone}</p>`;
        hidden.html(line1 + line2 + line3 + line4 + line5)
    });


});