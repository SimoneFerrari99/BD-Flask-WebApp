let i = 0; //variabile globale

function increment() { //funzione che incrementa la variabile globale i
	i += 1;
}

function removeElement(parentId, childId) { //rimuove un elemento HTML
	if (childId == parentId) {
		alert("The parent div cannot be removed.");
	} else {
		let child = document.getElementById(childId);
		let parent = document.getElementById(parentId);
		parent.removeChild(child);
	}
}

//persone è un dizionario di persone identificate da un id, tipo indica il tipo di quella persona ossia attore o regista
function addPeople(persone, tipo) { //funzione per aggiungere un campo attori o registi
	let span = document.createElement("SPAN"); //creo lo span
	span.setAttribute("id", "span_" + tipo + "_" + i);

	let label = document.createElement("LABEL"); //creo la label per attori o registi
	label.setAttribute("for", tipo + "_" + i);
	if (tipo.localeCompare("attori") == 0) {
		label.innerHTML = "Attore: ";
	} else {
		label.innerHTML = "Regista: ";
	}

	let select = document.createElement("SELECT"); //creo un menu a tendina
	select.setAttribute("name", tipo + "_" + i);
	select.setAttribute("id", tipo + "_" + i);

	for (let id in persone) {
		let opt = document.createElement("OPTION"); //creo le opzioni per il menu a tendina
		opt.setAttribute("value", id);
		opt.text = persone[id];
		select.appendChild(opt);
	}

	let addNewPeople = document.createElement("BUTTON"); //creo un bottone per renderizzare
	addNewPeople.setAttribute("type", "button");
	addNewPeople.innerHTML = "Aggiungi nuova persona";

	addNewPeople.setAttribute(
		"onclick",
		"window.location.href = '/aggiungi_persona'"
	);

	let remove = document.createElement("BUTTON"); //bottone per rimuovere la riga appena creata
	remove.innerHTML = "Rimuovi";
	let removeParent = '"' + tipo + '"';
	let removeChild = '"span_' + tipo + '_' + i + '"';
	remove.setAttribute("type", "button");
	remove.setAttribute(
		"onclick",
		"removeElement(" + removeParent + ", " + removeChild + ")"
	);

	//appendo tutti gli oggetti allo span
	span.appendChild(label);
	span.appendChild(select);
	span.appendChild(addNewPeople);
	span.appendChild(remove);
	span.appendChild(document.createElement("br"));
	increment();
	document.getElementById(tipo).appendChild(span);
}

//generi è un dizionario con i generi disponibili
function addGenre(generi) { //funzione per aggiungere un campo di selezione per il genere
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
