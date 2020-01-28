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
//     tables.each(function (index, element) {
//         $(element).removeClass('True');
//         let checkboxes = $('[type="checkbox"]')
//         console.log(checkboxes)
//     })
// });
// let check = $('#tables');
// if (reset.checked) {
//     check.attr('checked', false)
// }
//