{% extends "base.tpl" %}

{% block content %}
    {% include "data/patient.tpl" %}

    <hr />

    {% for prescription in prescriptions %}
        {% include "data/prescription.tpl" %}
    {% endfor %}
{% endblock %}
