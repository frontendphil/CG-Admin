<h1>{{ patient.get_gender() }} {{ patient.name }} {{ patient.surname }}</h1>

<hr />

<h2>Stammdaten</h2>

<table class="highlight-first">
    <tbody>
        <tr>
            <td>Geburtstag:</td>
            <td>{{ patient.get_birthday() }}</td>
        </tr>
        <tr>
            <td>Anschrift:</td>
            <td>{{ patient.address }}</td>
        </tr>
        <tr>
            <td>Telefon (privat):</td>
            <td>{{ patient.phone_private }}</td>
        </tr>
        <tr>
            <td>Telefon (gesch&auml;ftlich):</td>
            <td>{{ patient.phone_office }}</td>
        </tr>
        <tr>
            <td>Privatpatient:</td>
            <td>
                {% if patient.state == "p" %}
                    Ja
                {% else %}
                    Nein
                {% endif %}
            </td>
        </tr>
        <tr>
            <td>BG-Rezept:</td>
            <td>
                {% if patient.state == "b" %}
                    Ja
                {% else %}
                    Nein
                {% endif %}
            </td>
        </tr>
        {% if patient.state == "k" %}
            <tr>
                <td>Kasse:</td>
                <td>{{ insurance }}</td>
            </tr>
        {% endif %}
    </tbody>
</table>
