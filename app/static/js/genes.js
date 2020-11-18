$(function () {

  /* Functions */
    var NoResultsLabel = {label:"No Results", value:"No Results"};
    $( ".gene_autocomplete" ).autocomplete({
      source: "/test/gene-autocomplete",
      minLength: 0,
      response: function(event, ui) {
            if (ui.content.length === 0) {
                ui.content.push(NoResultsLabel)
            }
      },
      select: function (event, ui) {
            if (ui.item.label === NoResultsLabel.label) {
                event.preventDefault();
            }
        },
      focus: function (event, ui) {
            if (ui.item.label === NoResultsLabel.label) {
                event.preventDefault();
            }
      }
    }).focus(function(){
        $(this).autocomplete("search", $(this).val());
    });

    $(".gene_react").on("click", function(){
        var target = $(this).attr("data-target")
        var val = $(target).val()
        var url = $(this).attr("data-url")
        if (val){
            window.location.href = url + val;
        }
    })

});
