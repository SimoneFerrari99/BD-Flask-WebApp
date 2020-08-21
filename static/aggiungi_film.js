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

function addPeople(persone, tipo) {
	let span = document.createElement("SPAN");
	span.setAttribute("id", "span_" + tipo + "_" + i);

	let label = document.createElement("LABEL");
	label.setAttribute("for", tipo + "_" + i);
	if (tipo.localeCompare("attori") == 0) {
		label.innerHTML = "Attore: ";
	} else {
		label.innerHTML = "Regista: ";
	}

	let select = document.createElement("SELECT");
	select.setAttribute("name", tipo + "_" + i);
	select.setAttribute("id", tipo + "_" + i);

	for (let id in persone) {
		let opt = document.createElement("OPTION");
		opt.setAttribute("value", id);
		opt.text = persone[id];
		select.appendChild(opt);
	}

	let addNewPeople = document.createElement("BUTTON");
	addNewPeople.setAttribute("type", "button");
	addNewPeople.innerHTML = "Aggiungi nuova persona";

	addNewPeople.setAttribute(
		"onclick",
		"window.location.href = '/aggiungi_persona'"
	);

	let remove = document.createElement("BUTTON");
	remove.innerHTML = "Rimuovi";
	let removeParent = '"' + tipo + '"';
	let removeChild = '"span_' + tipo + '_' + i + '"';
	remove.setAttribute("type", "button");
	remove.setAttribute(
		"onclick",
		"removeElement(" + removeParent + ", " + removeChild + ")"
	);

	span.appendChild(label);
	span.appendChild(select);
	span.appendChild(addNewPeople);
	span.appendChild(remove);
	span.appendChild(document.createElement("br"));
	increment();
	document.getElementById(tipo).appendChild(span);
}

function addGenre(generi) {
	let span = document.createElement("SPAN");
	span.setAttribute("id", "span_genere_" + i);

	let label_genere = document.createElement("LABEL");
	label_genere.setAttribute("for", "generi_" + i);
	label_genere.innerHTML = "Genere: ";

	let genere = document.createElement("SELECT")
	genere.setAttribute("name", "generi_" + i);
	genere.setAttribute("id", "generi_" + i);

	for (let elem in generi) {
		let opt = document.createElement("OPTION");
		opt.setAttribute("value", generi[elem]);
		opt.text = generi[elem];
		genere.appendChild(opt);
	}

	let addNewGenre = document.createElement("BUTTON");
	addNewGenre.setAttribute("type", "button");
	addNewGenre.innerHTML = "Aggiungi nuovo genere";

	addNewGenre.setAttribute(
		"onclick",
		"window.location.href = '/aggiungi_genere'"
	);

	let remove = document.createElement("BUTTON");
	remove.innerHTML = "Rimuovi";
	let removeParent = '"generi"';
	let removeChild = '"span_genere_' + i + '"';
	remove.setAttribute("type", "button");
	remove.setAttribute(
		"onclick",
		"removeElement(" + removeParent + ", " + removeChild + ")"
	);

	span.appendChild(label_genere);
	span.appendChild(genere);
	span.appendChild(addNewGenre);
	span.appendChild(remove);
	span.appendChild(document.createElement("br"));
	increment();
	document.getElementById("generi").appendChild(span);

}
