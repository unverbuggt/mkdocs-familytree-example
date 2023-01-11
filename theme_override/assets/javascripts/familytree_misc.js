function lang_label(node) {
    if (node.is_union()) return;
    let label;
    label = node.get_name();
    label += "_"; //label_delimiter
    if (node.get_birth_year()) {
        label += node.get_birth_year().toString();
    }
    if (node.get_death_year()) {
        label += ' - ' + node.get_death_year().toString();
    }
    if (node.data.age) {
        label += ' (' + node.data.age.toString() + ')';
    } else if (node.data.deathplace) {
        label += ' (?)';
    } else if (node.get_birth_year()) {
        label += ' (ca. ' + (new Date().getFullYear() - node.get_birth_year()).toString() + ')';
    }

    return label;
};

function node_class(node) {
    // returns a node's css classes as a string
    if (node.is_union()) return;
    let classes = "";
    if (node.data.sex == 'f') {
        classes += 'person-f';
    } else if (node.data.sex == 'm') {
        classes += 'person-m';
    } else {
        classes += 'person';
    }
    if (node.is_extendable()) {
        classes += ' extendable';
    } else {
        classes += ' non-extendable';
    }
    return classes;
};

function familytree_size() {
  let footer =  document.getElementsByTagName('footer')[0];
  let offsets_footer = footer.getBoundingClientRect();
  let w3_main = document.getElementsByClassName('w3-main')[0].children[0]; 
  let offsets_w3_main = w3_main.getBoundingClientRect();
  let svg = document.getElementById('FT-main');

  //adjust height of main container
  w3_main.style.height = (offsets_footer.y - offsets_w3_main.y).toString() + "px";
  svg.style.width = (w3_main.offsetWidth + offsets_w3_main.x).toString() + "px";
  svg.style.height = (w3_main.offsetHeight + offsets_w3_main.y).toString() + "px";
}

function familytree_init() {
  //send footer to bottom
  let footer =  document.getElementsByTagName('footer')[0];
  if (footer.className.indexOf("w3-bottom") == -1) {
    footer.className += " w3-bottom";
    footer.style = 'width: -moz-available; width: -webkit-fill-available;';
  }
  let offsets_footer = footer.getBoundingClientRect();

  let w3_main = document.getElementsByClassName('w3-main')[0].children[0]; 
  let offsets_w3_main = w3_main.getBoundingClientRect();

  //adjust height of main container
  w3_main.style.height = (offsets_footer.y - offsets_w3_main.y).toString() + "px";

  //svg object to hold the family tree
  let svg = d3.select('#FT-main')
    .attr("width", w3_main.offsetWidth + offsets_w3_main.x)
    .attr("height", w3_main.offsetHeight + offsets_w3_main.y);

  //make family tree object
  let FT = new FamilyTree(data, svg)
    .node_class(node => node_class(node))
    .node_size(node => node.is_union() ? 0 : 15)
    .tooltip(node => lang_tooltip(node))
    .node_label(node => lang_label(node));

  //draw family tree
  FT.draw();
  
  window.onresize = familytree_size;
};