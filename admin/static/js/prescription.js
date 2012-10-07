(function() {

    $(document).ready(function() {
        if($(".add_new_doc").val() !== "1") {
            $(".inline-form").hide();
        } else {
            $(".existing-doc").hide();
        }

        $(".add-doc").click(function() {
            $(".inline-form").show("slow");
            $(".existing-doc").hide("slow");

            $(".add_new_doc").val(1);

            return false;
        });

        $(".inline-form button.abort").click(function() {
            $(".inline-form").hide("slow");
            $(".existing-doc").show("slow");

            $(".add_new_doc").val(0);

            return false;
        });

        $("button.skip").click(function() {
            window.location.href = CG.ADD_PATIENT + "/confirm";
        });
    });

}());