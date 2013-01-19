(function($) {

    $(document).ready(function() {

        var insurance = $(".insurance-group");
        var radio = $("form input[type=radio]:checked");
        if(radio.val() === "p" || radio.val() === "b" || radio.length === 0) {
            insurance.hide();
        }

        $("form :radio").each(function(index, radio) {
            radio = $(radio);

            if(radio.val() === "p" || radio.val() === "b") {
                radio.on("click", function() {
                    insurance.hide("slow");
                })
            } else {
                radio.on("click", function() {
                    insurance.show("slow");
                })
            }
        });

        var form = $("form.add-patient");

        form.find(".form-actions input").each(function(i) {
            $(this).on("click", function(e) {
                e.preventDefault();

                var target = $(this).attr("target");

                form.attr("action", target);
                form.submit();
            });
        });
    });

}(window.jQuery));