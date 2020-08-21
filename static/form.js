var i = 0;

function increment() {
	i += 1;
}

function removeElement(parentDiv, childDiv) {
	if (childDiv == parentDiv) {
		alert("The parent div cannot be removed.");
	} else if (document.getElementById(childDiv)) {
		var child = document.getElementById(childDiv);
		var parent = document.getElementById(parentDiv);
		parent.removeChild(child);
	} else {
		alert("Child div has already been removed or does not exist.");
		return false;
	}
}

function addActor(attori) {
	var span = document.createElement("span");
	var select = document.createElement("select");
	var label = document.createElement("LABEL");
	label.setAttribute("for", "attore_" + i);
	label.innerHTML = "Attore: ";
	select.setAttribute("name", "attore_" + i);
	select.setAttribute("id", "attore_" + i);
	for (let id in attori) {
		var opt = document.createElement("option");
		opt.setAttribute("value", id);
		opt.text = attori[id];
		select.appendChild(opt);
	}
	span.appendChild(label);
	label.appendChild(select);
	span.appendChild(document.createElement("br"));
	increment();
	//g.setAttribute("onclick", "removeElement('myForm','id_" + i + "')");
	//r.appendChild(g);
	span.setAttribute("id", "id_" + i);
	document.getElementById("select").appendChild(span);
}
