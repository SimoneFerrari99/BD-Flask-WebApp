let i = 0;

function increment() {
	i += 1;
}

function removeElement(parentDiv, childDiv) {
	if (childDiv == parentDiv) {
		alert("The parent div cannot be removed.");
	} else {
		let child = document.getElementById(childDiv);
		let parent = document.getElementById(parentDiv);
		parent.removeChild(child);
	}
}

function addProjection(sale) {
	let span = document.createElement("SPAN");
	span.setAttribute("id", "span_proiezione_" + i);

	let label_sala = document.createElement("LABEL");
	label_sala.setAttribute("for", "sala_" + i);
	label_sala.innerHTML = "Sala: ";

	let sala = document.createElement("SELECT")
	sala.setAttribute("name", "sala_" + i);
	sala.setAttribute("id", "sala_" + i);

	for (let elem in sale) {
		let opt = document.createElement("OPTION");
		opt.setAttribute("value", sale[elem]);
		opt.text = sale[elem];
		sala.appendChild(opt);
	}

	let label_data = document.createElement("LABEL");
	label_data.setAttribute("for", "data_" + i);
	label_data.innerHTML = "Data: ";

	let data = document.createElement("INPUT");
	data.setAttribute("type", "date")
	data.setAttribute("name", "data_" + i);
	data.setAttribute("id", "data_" + i);

	let label_ora = document.createElement("LABEL");
	label_ora.setAttribute("for", "ora_" + i);
	label_ora.innerHTML = "Orario: ";

  let ora = document.createElement("INPUT");
	ora.setAttribute("type", "time")
  ora.setAttribute("name", "ora_" + i);
  ora.setAttribute("id", "ora_" + i);

	let remove = document.createElement("BUTTON");
	remove.innerHTML = "Rimuovi";
	let removeParent = '"proiezioni"';
	let removeChild = '"span_proiezione_' + i + '"';
	remove.setAttribute("type", "button");
	remove.setAttribute(
		"onclick",
		"removeElement(" + removeParent + ", " + removeChild + ")"
	);

	span.appendChild(label_sala);
	span.appendChild(sala);
	span.appendChild(label_data);
	span.appendChild(data);
	span.appendChild(label_ora);
	span.appendChild(ora);
	span.appendChild(remove);
	span.appendChild(document.createElement("br"));
	increment();
	document.getElementById("proiezioni").appendChild(span);
}