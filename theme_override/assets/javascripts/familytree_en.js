function lang_tooltip(node) {
    if (node.is_union()) return;
    let content = '';
    if (node.data.thumb) {
        content += '<table><tr><td><img src="'  + base_url + '/' + node.data.thumb + '"></td><td>';
    }
    content += '<span style="margin-left: 2.5px;"><b>' + node.data.longname;
    if (node.data.birthname) {
        if (node.data.sex == 'f') {
            content += ' née ' + node.data.birthname;
        } else if (node.data.sex == 'm') {
            content += ' né ' + node.data.birthname;
        }
    }
    content += '</b></span><br>';
    content += '<table style="margin-top: 2.5px;">';
    if (node.get_birth_year() || node.data.birthplace) {
        content += '<tr><td>born';
        if (node.get_birth_year()) {
            content += ' ' + node.get_birth_year().toString();
        }
        if (node.data.birthplace) {
            content += ' in ' + node.data.birthplace;
        }
        content += '</td></tr>';
    }
    if (node.get_death_year() || node.data.deathplace) {
        content += '<tr><td>deceased';
        if (node.get_death_year()) {
            content += ' ' + node.get_death_year().toString();
        }
        if (node.data.deathplace) {
            if (node.data.deathplace == "?" && !node.get_death_year()) {
                content += ' (presumably)';
            } else {
                content += ' in ' + node.data.deathplace;
            }
        }
        content += '</td></tr>';
    }
    if (node.data.age) {
        content += '<tr><td>age ' + node.data.age.toString() + ' years</td></tr>';
    } else if (node.data.deathplace) {
        content += '<tr><td>age unknown</td></tr>';
    } else if (node.get_birth_year()) {
        content += '<tr><td>age (approx.) ' + (new Date().getFullYear() - node.get_birth_year()).toString() + ' years</td></tr>';
    }
    if (node.data.job) {
        content += '<tr><td>occupation: ' + node.data.job + '</td></tr>';
    }
    if (node.data.mageab) {
        content += '<tr><td>mother\'s age at birth: ' + node.data.mageab + '</td></tr>';
    }
    if (node.data.fageab) {
        content += '<tr><td>father\'s age at birth: ' + node.data.fageab + '</td></tr>';
    }
    content += '</table>';
    if (node.data.thumb) {
        content += '</td></tr></table>';
    }
    return content;
};
