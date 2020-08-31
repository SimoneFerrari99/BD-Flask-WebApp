//funzione per rimuovere i campi option di una select (chiamata quando cambio scelta dal primo campo della rimuovi film)
function removeProiezioni() {
	let proiezioni_sel = document.getElementById("proiezione"); //prendo elemento html grazie al suo id
	for (let i = proiezioni_sel.length - 1; i >= 0; i--) {
		proiezioni_sel[i].parentNode.removeChild(proiezioni_sel[i]);
	}
}

//funzione che, al cambiamento del valore selezionato del film, genera i campi per selezionare la proiezione da eliminare visualizzando solamente le proiezioni relative a quel film
function selectProiezioni(proiezioni) {
	removeProiezioni();
	let select = document.getElementById("film");
	let currently_selected = select.options[select.selectedIndex].value;
	let proiezioni_sel = document.getElementById("proiezione");
	for (let i = 0; i < proiezioni.length; i++) {
		let proiezione = proiezioni[i];
		if (currently_selected == proiezione.id_film) {
			let content = proiezione.data + " " + proiezione.ora_inizio + " sala " + proiezione.sala;
			console.log(content);
			let opt = document.createElement("option");
			opt.setAttribute("value", proiezione.id_proiezione);
			opt.text = content;
			proiezioni_sel.appendChild(opt);
		}
	}
}
