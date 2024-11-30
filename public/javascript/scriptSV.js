/*spunta verde */
document.addEventListener('DOMContentLoaded', () => {
    // Seleziona tutte le card
    const cards = document.querySelectorAll('.carousel-item');

    // Aggiungi l'evento click a ciascuna card
    cards.forEach(card => {
        card.addEventListener('click', () => {
            // Rimuovi la classe 'selected' da tutte le card
            cards.forEach(c => c.classList.remove('selected'));

            // Aggiungi la classe 'selected' alla card cliccata
            card.classList.add('selected');
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const carouselItems = document.querySelectorAll('.carousel-item');
    let selectedArgomento = '';  // Variabile per memorizzare l'argomento selezionato

    // Gestione della selezione nel carousel
    carouselItems.forEach((item) => {
        item.addEventListener('click', () => {
            // Ottieni il titolo del carousel selezionato
            selectedArgomento = item.querySelector('.carousel-item__details--title').innerText;

            // Aggiorna il campo nascosto del form
            document.getElementById('selectedArgomento').value = selectedArgomento;
        });
    });

    // Gestione dell'invio del form
    document.getElementById('scenarioForm').addEventListener('submit', async (event) => {
        event.preventDefault();  // Previene il comportamento predefinito del form

        // Crea un oggetto FormData con i dati del form
        const formData = new FormData(event.target);

        // Invia i dati al server tramite fetch (POST)
        const response = await fetch('/scenario', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();  // Converte la risposta del server in JSON

        // Mostra il messaggio di risposta del server
        document.getElementById('response').innerText = result.message || result.error;
    });
});

window.onload = function() {
    // Verifica se l'URL contiene il parametro "error=password"
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('error') === 'DatiObbligatori') {
        // Mostra il pop-up
        alert("Tutti i campi sono obbligatori. Riprova.");
    }
    if (urlParams.get('error') === 'formatoTitolo') {
        alert("Il formato del titolo è errato. Riprova.");
    }
    else if (urlParams.get('error') === 'formatoDescrizione') {
        alert("Il formato della descrizione è errato. Riprova.");
    }
    else if (urlParams.get('error') === 'argomentoNonValido') {
        alert("L'argomento non è valido. Riprova.");
    }
};

document.addEventListener("DOMContentLoaded", function() {
    const createScenarioButton = document.querySelector('.button_2'); // Seleziona il bottone CREA SCENARIO
    const formScenario = document.getElementById('formScenario'); // Seleziona il form

    createScenarioButton.addEventListener('click', function(event) {
        event.preventDefault(); // Previene l'invio predefinito del form

        // Seleziona il radio button selezionato
        const selectedRadio = document.querySelector('input[name="engine"]:checked');

        if (selectedRadio) {
            // Crea o aggiorna un input nascosto nel form
            let inputModalita = document.querySelector('input[name="modalità"]');
            if (!inputModalita) {
                inputModalita = document.createElement('input');
                inputModalita.type = 'hidden';
                inputModalita.name = 'modalità';
                formScenario.appendChild(inputModalita);
            }
            inputModalita.value = selectedRadio.nextElementSibling.querySelector('.radio-label').innerText.trim(); // Ottiene il valore del label associato

            // Invia il form
            formScenario.submit();
        } else {
            alert('Seleziona una modalità prima di procedere!');
        }
    });
});


