function removeProiezioni() {
	let proiezioni_sel = document.getElementById("proiezione");
	for (let i = proiezioni_sel.length - 1; i >= 0; i--) {
		proiezioni_sel[i].parentNode.removeChild(proiezioni_sel[i]);
	}
}

function selectProiezioni(proiezioni) {
	removeProiezioni();
	let select = document.getElementById("film");
	let currently_selected = select.options[select.selectedIndex].value;
	let proiezioni_sel = document.getElementById("proiezione");
	for (let i = 0; i < proiezioni.length; i++) {
		let proiezione = proiezioni[i];
		if (currently_selected == proiezione.id_film) {
			let content =
				proiezione.data +
				" " +
				proiezione.ora_inizio +
				" sala " +
				proiezione.sala;
			console.log(content);
			let opt = document.createElement("option");
			opt.setAttribute("value", proiezione.id_proiezione);
			opt.text = content;
			proiezioni_sel.appendChild(opt);
		}
	}
}
