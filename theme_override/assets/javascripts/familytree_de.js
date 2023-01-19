function lang_tooltip(node) {
    if (node.is_union()) return;
    let content = '';
    if (node.data.thumb) {
        content += '<table><tr><td><img src="'  + base_url + '/' + node.data.thumb + '"></td><td>';
    }
    content += '<span style="margin-left: 2.5px;"><b>' + node.data.longname;
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
    if (node.data.job) {
        content += '<tr><td>Beruf: ' + node.data.job + '</td></tr>';
    }
    if (node.data.mageab | node.data.fageab) {
        content += '<tr class="w3-tiny"><td>Alter der Eltern (Geburt):';
        if (node.data.mageab) {
            content += ' ' + node.data.mageab + '(M)';
        }
        if (node.data.fageab) {
            content += ' ' + node.data.fageab + '(V)';
        }
        content += '</td></tr>';
    }
    content += '</table>';
    if (node.data.thumb) {
        content += '</td></tr></table>';
    }
    return content;
};
