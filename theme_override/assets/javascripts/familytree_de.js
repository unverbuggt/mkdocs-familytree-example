function lang_tooltip(node) {
    if (node.is_union()) return;
    let content;
    content = '<span style="margin-left: 2.5px;"><b>' + node.data.longname;
    if (node.data.birthname) {
        content += ' geb. ' + node.data.birthname;
    }
    content += '</b></span><br>';
    content += '<table style="margin-top: 2.5px;">';
    if (node.get_birth_year() || node.data.birthplace) {
        content += '<tr><td>geboren';
        if (node.get_birth_year()) {
            content += ' ' + node.get_birth_year().toString();
        }
        if (node.data.birthplace) {
            content += ' in ' + node.data.birthplace;
        }
        content += '</td></tr>';
    }
    if (node.get_death_year() || node.data.deathplace) {
        content += '<tr><td>verstorben';
        if (node.get_death_year()) {
            content += ' ' + node.get_death_year().toString();
        }
        if (node.data.deathplace) {
            if (node.data.deathplace == "?" && !node.get_death_year()) {
                content += ' (vermutlich)';
            } else {
                content += ' in ' + node.data.deathplace;
            }
        }
        content += '</td></tr>';
    }
    if (node.data.age) {
        content += '<tr><td>im Alter von ' + node.data.age.toString() + ' Jahren</td></tr>';
    } else if (node.data.deathplace) {
        content += '<tr><td>Alter unbekannt</td></tr>';
    } else if (node.get_birth_year()) {
        content += '<tr><td>Alter ca. ' + (new Date().getFullYear() - node.get_birth_year()).toString() + ' Jahre</td></tr>';
    }
    content += '</table>';

    return content;
};
