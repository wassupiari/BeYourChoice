// Aggiungi evento per la selezione delle card con spunta verde
document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll('.carousel-item');

    cards.forEach(card => {
        card.addEventListener('click', () => {
            // Rimuovi la classe 'selected' da tutte le card
            cards.forEach(c => c.classList.remove('selected'));

            // Aggiungi la classe 'selected' alla card cliccata
            card.classList.add('selected');

            // Aggiorna il campo nascosto dell'argomento
            const selectedArgomento = card.querySelector('.carousel-item__details--title').innerText;
            document.getElementById('selectedArgomento').value = selectedArgomento;
        });
    });
});

// Configura Toastr per notifiche
toastr.options = {
    closeButton: true,
    progressBar: true,
    positionClass: "toast-bottom-center",
    timeOut: 5000,
    extendedTimeOut: 1000,
    showMethod: "fadeIn",
    hideMethod: "fadeOut",
};

document.addEventListener("DOMContentLoaded", function () {
    // Configura Toastr
    toastr.options = {
        closeButton: true,
        progressBar: true,
        positionClass: "toast-bottom-center",
        timeOut: 5000,
        extendedTimeOut: 1000,
        showMethod: "fadeIn",
        hideMethod: "fadeOut",
    };

    // Mostra notifiche Toastr basate sui parametri dell'URL
    const urlParams = new URLSearchParams(window.location.search);

    if (urlParams.has('error')) {
        const errorType = urlParams.get('error');
        switch (errorType) {
            case 'DatiObbligatori':
                toastr.error("Tutti i campi sono obbligatori. Riprova.");
                break;
            case 'formatoTitolo':
                toastr.error("Il formato del titolo è errato. Riprova.");
                break;
            case 'formatoDescrizione':
                toastr.error("Il formato della descrizione è errato. Riprova.");
                break;
            case 'argomentoNonValido':
                toastr.error("L'argomento selezionato non è valido. Riprova.");
                break;
            default:
                toastr.error("Si è verificato un errore sconosciuto. Riprova.");
                break;
        }

        // Rimuove il parametro "error" dall'URL
        const cleanUrl = window.location.href.split('?')[0];
        window.history.replaceState({}, document.title, cleanUrl);
    }

    // Gestione del click sul bottone CREA SCENARIO
    const createScenarioButton = document.querySelector('.button_2'); // Bottone CREA SCENARIO
    const formScenario = document.getElementById('formScenario'); // Form principale

    createScenarioButton.addEventListener('click', function (event) {
        event.preventDefault(); // Previeni l'invio predefinito del form

        // Raccogli i dati dal form
        const titolo = document.querySelector('input[name="titolo"]').value.trim();
        const descrizione = document.querySelector('textarea[name="descrizione"]').value.trim();
        const argomento = document.getElementById('selectedArgomento').value.trim();
        const modalitaElement = document.querySelector('input[name="engine"]:checked');
        const modalita = modalitaElement
            ? modalitaElement.nextElementSibling.querySelector('.radio-label').innerText.trim()
            : '';

        // Validazione dei campi
        if (!titolo) {
            toastr.error("Il campo Titolo è obbligatorio. Riprova.");
            return;
        }

        if (!descrizione) {
            toastr.error("Il campo Descrizione è obbligatorio. Riprova.");
            return;
        }

        if (!argomento) {
            toastr.error("Seleziona un argomento per procedere.");
            return;
        }

        if (!modalita) {
            toastr.error("Seleziona una modalità prima di procedere.");
            return;
        }

        // Controlla se l'input nascosto per la modalità esiste già
        let inputModalita = document.querySelector('input[name="modalita"]');
        if (!inputModalita) {
            inputModalita = document.createElement('input');
            inputModalita.type = 'hidden';
            inputModalita.name = 'modalita';
            formScenario.appendChild(inputModalita);
        }

        // Imposta il valore della modalità selezionata
        inputModalita.value = modalita;

        // Invia il form utilizzando la logica originale (submit)
        formScenario.submit();
    });
});
