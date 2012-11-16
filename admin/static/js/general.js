(function($) {

    $(document).ready(function() {
        var getAttachment = function() {
            if(window.URL_ATTACHMENT) {
                return [window.URL_ATTACHMENT];
            }

            var url = window.location.href;
            var parts = url.split("#");

            return parts.slice(1);
        };

        var updateTarget = function(link, attr) {
            var target = link.attr(attr);

            if(target) {
                target = target + "#";
            } else {
                target = "";
            }

            link.attr(attr, target + getAttachment().join("#"));
        };

        $("a[rel=abort], a[rel=forward]").each(function(index, a) {
            updateTarget($(a), "href");
        });

        $("form[rel=forward]").each(function(index, form) {
            form = $(form);

            var action = form.attr("action");

            form.attr("action", action + "?forward=" + getAttachment().join("#"));
        });

        $("button[rel=forward], button[rel=abort]").each(function(index, btn){
            updateTarget($(btn), "target");
        });

        $("a[rel=delete]").each(function(index, a) {
            a = $(a);

            var after = a.attr("after");
            var target = a.attr("href");

            if(!target) {
                target = "";
            }

            if(after) {
                a.attr("href", target + "?redirect=" + after);
            }
        });

        $("button").each(function(index, btn) {
            btn = $(btn);

            var target = btn.attr("target");

            if(target) {
                btn.click(function(e) {
                    e.preventDefault();

                    window.location.href = target;

                    return false;
                });

                return;
            }

            var type = btn.attr("type");

            if(type && type === "submit") {
                var form = btn.parents("form");
                var warn = btn.attr("warning");

                if(form) {
                    btn.click(function() {
                        if(warn && !window.confirm(warn)) {
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