<h2>Rezept vom {{ prescription.get_date() }}</h2>

<table class="highlight-first">
    <tbody>
        <tr>
            <td>Diagnose:</td>
            <td>{{ prescription.diagnosis }}</td>
        </tr>
        <tr>
            <td>Behandlung:</td>
            <td>{{ prescription.cure }}</td>
        </tr>
        <tr>
            <td>Art:</td>
            <td>{{ prescription.get_kind() }}</td>
        </tr>
        <tr>
            <td>Hausbesuche:</td>
            <td>
                {% if prescription.visit %}
                    Ja
                {% else %}
                    Nein
                {% endif %}
            </td>
        </tr>
        <tr>
            <td>Therapiebericht:</td>
            <td>
                {% if prescription.report %}
                    Ja
                {% else %}
                    Nein
                {% endif %}
            </td>
        </tr>
        <tr>
            <td>Verordnungsmenge:</td>
            <td>{{ prescription.amount }}</td>
        </tr>
        <tr>
            <td>Anzahl pro Woche:</td>
            <td>{{ prescription.count }}</td>
        </tr>
        <tr>
            <td>Indikationsschl&uuml;ssel:</td>
            <td>{{ prescription.indicator }}</td>
        </tr>
        <tr>
            <td>Verschreibender Arzt:</td>
            <td>
                {% if prescription.doctor %}
                    {{ prescription.doctor }}
                {% endif %}
            </td>
        </tr>
        <tr>
            <td valign="top">Termine:</td>
            <td>{{ prescription.appointments }}</td>
        </tr>
    </tbody>
</table>
