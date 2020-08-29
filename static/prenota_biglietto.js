let importo = 0;
let posti_sel = [];

function alertError(messaggio) {
  alert(messaggio);
}

function selezionaPosto(id){
  posti_sel.push(id);
  importo += 5;
  let totale = document.getElementById("importo");
  totale.innerHTML = importo + ".0€";
  let bottone = document.getElementById(id);
  bottone.style.backgroundColor = "blue";
  bottone.setAttribute( "onClick", "deselezionaPosto(id)");
}

function deselezionaPosto(id){
  posti_sel.pop(id);
  importo -= 5;
  let totale = document.getElementById("importo");
  totale.innerHTML = importo + ".0€";
  let bottone = document.getElementById(id);
  bottone.style.backgroundColor = "green";
  bottone.setAttribute( "onClick", "selezionaPosto(id)");
}

function invia(id_proiezione){

  let prenotazione = {
    posti: posti_sel,
    totale: importo
  };
  id = parseInt(id_proiezione);
  fetch("/prenota_biglietto/"+id,{
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(prenotazione)
  }).then(function (response){
    return response.text();
  }).then(function (text){
    if(text.localeCompare("Conflict") == 0){
      alertError("Saldo insufficiente, prego ricaricare il saldo.");
      window.location.href = "/ricarica_saldo";
    }
    else{
      window.location.href = "/prenota_biglietto/"+id;
    }
  }).catch(function (error){
    console.error(error);
  });
}
