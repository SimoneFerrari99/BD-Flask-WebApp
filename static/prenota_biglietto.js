let importo = 0;
let posti_sel = [];

function selezionaPosto(id){
  posti_sel.push(id);
  importo += 5;
  let totale = document.getElementById("importo");
  totale.innerHTML = importo + ".0€";
  let bottone = document.getElementById(id);
  bottone.style.backgroundColor = "red";
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

function invia(){

  let prenotazione = {
    posti: posti_sel,
    totale: importo
  };
  fetch("/prenota_biglietto",{
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(prenotazione)
  }).then(function (response){
    return response.text();
  }).then(function (text){
    window.location.href = "/";
  }).catch(function (error){
    console.error(error);
  });
}
