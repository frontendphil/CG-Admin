(function($) {

    $(document).ready(function() {
        var updateTarget = function(link, attr) {
            var url = window.location.href;
            var parts = url.split("#");

            var remainder = parts.slice(1);
            var target = link.attr(attr);

            if(target) {
                target = target + "#";
            } else {
                target = "";
            }

            link.attr(attr, target + remainder.join("#"));
        };

        $("a[rel=abort], a[rel=forward]").each(function(index, a) {
            updateTarget($(a), "href");
        });

        $("button[rel=forward], button[rel=abort]").each(function(index, btn){
            updateTarget($(btn), "target");
        });

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