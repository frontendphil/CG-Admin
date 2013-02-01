<html>
    <head>
        <title>{% block title %}{% endblock %}</title>
        <style type="text/css">
            table.highlight-first td:first-child {
                width: 25%;
                font-weight: bold;
            }

            {% block style %}
            {% endblock %}
        </style>
    </head>
    <body>
        {% block content %}
        {% endblock %}
    </body>
</html>
