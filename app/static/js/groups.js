$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      beforeSend: function () {
        $("#modal-group").modal("show");
      },
      success: function (data) {
        $("#modal-group .modal-content").html(data);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("data-url"),
      data: form.serialize(),
      type: form.attr("method"),
      success: function (data) {
        if (data.status == 'ok') {
            $('#Modal').modal('hide');
            window.location = data.redirect;
        } else {
            var obj = JSON.parse(data);
            for (var key in obj) {
              if (obj.hasOwnProperty(key)) {
                var value = obj[key];
              }
            }
            $('.help-block').remove()
            $('<p class="help-block" style="color:red">' + value + '</p>')
                .insertAfter('#' + key);
            $('.form-group').addClass('has-error')
        }
      }
    });
    return false;
  };

  /* Binding */
    $(".tab-content").on("click", ".js-form", loadForm);
    $("#modal-group").on("submit", ".js-form", saveForm);
});
