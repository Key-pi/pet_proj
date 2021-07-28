// $(function () {
//
// var loadForm = function () {
//   var btn = $(this)
//   $.ajax({
//     url: btn.attr("data-url"),
//     type: 'get',
//     dataType: 'json',
//     beforeSend: function () {
//       $("#modal-board").modal("show");
//     },
//     success: function (data) {
//       $("#modal-board .modal-content").html(data.html_form);
//     }
//   });
// }
//
//
// var saveForm = function () {
//     var form = $(this);
//     $.ajax({
//       url: form.attr("action"),
//       data: form.serialize(),
//       type: form.attr("method"),
//       dataType: 'json',
//       success: function (data) {
//
//         if (data.form_is_valid) {
//
//
//           if(form.attr("action").split("/")[3] === "delete"){
//             $(`#board_${form.attr("action").split("/")[2]}`).remove()
//           }
//
//
//           console.log("action", form.attr("action").split("/")[3])
//           var modal = $(".modal-content")
//           var modalContent = modal[0].innerHTML
//           var newModal = modalContent + `
//             <div style="background-color: seagreen; padding: 20px; text-align: right;">
//                ${
//                   form.attr("action").split("/")[3] === "update" ?
//                   "Has been updated!" :
//                   form.attr("action").split("/")[3] === "delete" ?
//                   "Has been deleted!" :
//                   "Has been created!"
//               }
//             </div>
//           `
//           modal[0].innerHTML = newModal
//           console.log(newModal)
//
//           setTimeout(function() {
//             $("#modal-board").modal("hide")
//           }, 2000)
//
//         }
//         else {
//         }
//       }
//     });
//
//
//
//     return false;
//   }
//
//
//   $(".js-create-board").click(loadForm);
//   $("#modal-board").on("submit", ".js-board-create-form", saveForm);
//
//
//   $("#board-table").on("click", ".js-update-board", loadForm);
//   $("#modal-board").on("submit", ".js-board-update-form", saveForm);
//
//
//   $("#board-table").on("click", ".js-delete-board", loadForm);
//   $("#modal-board").on("submit", ".js-board-delete-form", saveForm);
// });

$(function () {
  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-board").modal("show");
      },
      success: function (data) {
        $("#modal-board .modal-content").html(data.html_form);
      }
    });
  };
  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          console.log("action", form.attr("action").split("/")[3])
          var modal = $(".modal-content")
          var modalContent = modal[0].innerHTML
          var newModal = modalContent + `
          <div style="background-color: #2e8b57; padding: 20px; text-align: right;">
            ${
              form.attr("action").split("/")[3] === "update" ?
                  "Has been updated!" :
                  form.attr("action").split("/")[3] === "delete" ?
                      "Has been deleted!" :
                      "Has been created!"
          }
          </div>
           `
        modal[0].innerHTML = newModal
           setTimeout(function() {
         $("#modal-board").modal("hide")
         }, 2000)


          $("#board-table tbody").html(data.html_partial_board);
          // $("#modal-board").modal("hide");
        }
        else {
          $("#modal-board .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };
  $(".js-create-board").click(loadForm);
  $("#modal-board").on("submit", ".js-board-create-form", saveForm);
  $("#board-table").on("click", ".js-update-board", loadForm);
  $("#modal-board").on("submit", ".js-board-update-form", saveForm);
  $("#board-table").on("click", ".js-delete-board", loadForm);
  $("#modal-board").on("submit", ".js-board-delete-form", saveForm);
});