(function($) {

    $(document).ready(function() {
        $("button").each(function(index, btn) {
            btn = $(btn);

            var target = btn.attr("target");

            if(target) {
                btn.click(function(e) {
                    e.preventDefault()

                    window.location.href = target;

                    return false;
                });

                return;
            }

            var type = btn.attr("type");

            if(type && type == "submit") {
                var form = btn.parents("form");
                var warn = btn.attr("warning");

                if(form) {
                    btn.click(function() {
                        if(warn && !confirm(warn)) {
                            return false;
                        }

                        form.submit();

                        return false;
                    });
                }

                return;
            }

            var dataToggle = btn.attr("data-toggle");

            if(!dataToggle) {
                btn.click(function(e) {
                    e.preventDefault();

                    return false;
                });
            }
        });
    });

}(window.jQuery));