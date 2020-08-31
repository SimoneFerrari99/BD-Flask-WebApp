let importo = 0;
let posti_sel = [];

function alertError(messaggio) { //funzione per visualizzare un popup con messaggio d'errore
  alert(messaggio);
}

//funzione per selezionare il posto
function selezionaPosto(id){
  posti_sel.push(id);
  importo += 5;
  let totale = document.getElementById("importo");
  totale.innerHTML = importo + ".0€";
  let bottone = document.getElementById(id);
  bottone.style.backgroundColor = "blue";
  bottone.setAttribute( "onClick", "deselezionaPosto(id)");
}

//funzione per deselezionare il posto
function deselezionaPosto(id){
  posti_sel.pop(id);
  importo -= 5;
  let totale = document.getElementById("importo");
  totale.innerHTML = importo + ".0€";
  let bottone = document.getElementById(id);
  bottone.style.backgroundColor = "green";
  bottone.setAttribute( "onClick", "selezionaPosto(id)");
}

//funzione per l'invio dei posti selezionati e dell'importo totale al backend, utilizzando Fetch API
function invia(id_proiezione){
  let prenotazione = { //dizionario
    posti: posti_sel,
    totale: importo
  };
  id = parseInt(id_proiezione); //mi serve intero, no stringa
  fetch("/prenota_biglietto/"+id,{ //a che pagina inoltrare la richiesta della prenotazione (Route python)
    method: "POST", //metodo post
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(prenotazione) //converte in JSON la prenotazione (JSON Tipo javascript strano, simile ad un dizionario)
  }).then(function (response){ //anonymous class, prende una risposta (tipo return 200 OK)
    return response.text(); //returna il testo  della risposta "OK", "Conflict", ...
  }).then(function (text){ //prende in input la conversione
    if(text.localeCompare("Unassigned") == 0){ //confronto la stringa con unassignet
      alertError("Saldo insufficiente, prego ricaricare il saldo."); //saldo insuff
      window.location.href = "/ricarica_saldo"; //rimando al ricarica al saldo
    }
    else{
      if((text.localeCompare("Conflict") == 0)){ //se è conflict
        alertError("Qualcosa è andato storto :( riprovare."); //qualcosa non va
      }
      window.location.href = "/prenota_biglietto/"+id; //sia che sia conflict che ok, vado al prenota biglietto
    }
  }).catch(function (error){ //se catturo un errore
    console.error(error); //scrivo a console l'errore
  });
}
