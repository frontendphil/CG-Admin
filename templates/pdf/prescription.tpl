{% extends "base.tpl" %}

{% block content %}
    {% include "data/patient.tpl" %}

    <hr />

    {% include "data/prescription.tpl" %}
{% endblock %}
