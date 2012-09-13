(function() {

    $(document).ready(function() {

        var insurance = $(".insurance-group");
        var radio = $("form input[type=radio]:checked");
        if(radio.val() === "p" || radio.length === 0) {
            insurance.hide();
        }

        $("form :radio").each(function(index, radio) {
            radio = $(radio);

            if(radio.val() === "p") {
                radio.on("click", function() {
                    insurance.hide("slow");
                })
            } else {
                radio.on("click", function() {
                    insurance.show("slow");
                })
            }
        });

        $("form button[type=submit]").on("click", function(e) {
            $("form").attr("action", "/add/patient/?next=add_prescription");
        })

        $("form button[type=button]").on("click", function() {
            $("form").attr("action", "/add/patient/");

            $("form").submit();
        })
    });

}());