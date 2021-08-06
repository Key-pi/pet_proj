$(function () {

  /* Functions */

  var loadForm = function () {
    // debugger
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-contact .modal-content").html("");
        $("#modal-contact").modal("show");
      },
      success: function (data) {
        $("#modal-contact .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    // var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
                  console.log('yayayayayayayayayaaya')

        if (data.form_is_valid) {
          $(".modal-content").html(data.html_partial_board);
          $(".js-contact-form").modal("hide");
        }
        else {
          $("#modal-body .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create book
  $(".js-contact").click(loadForm);
  // $(".js-contact-form").click(saveForm);
    $("#modal-board").on("submit", ".js-contact-form", saveForm);
  // $(".js-contact-form").submit(saveForm);

  // Update book

});