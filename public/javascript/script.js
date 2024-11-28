//click su accedi e registrati nel container con immagine
    document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("container");
    const registerBtn = document.getElementById("register");
    const loginBtn = document.getElementById("login");

    // Aggiungi classe active per mostrare il form di registrazione
    registerBtn.addEventListener("click", () => {
        container.classList.add("active");
    });

    // Rimuovi classe active per tornare al form di accesso
    loginBtn.addEventListener("click", () => {
        container.classList.remove("active");
    });
});

// Funzione per calcolare la data limite (12 anni fa) e impostarla come massimo
        document.addEventListener('DOMContentLoaded', function() {
            const dataInput = document.getElementById('data');
            const today = new Date();

            // Calcola la data di 12 anni fa
            const twelveYearsAgo = new Date();
            twelveYearsAgo.setFullYear(today.getFullYear() - 12);

            // Formatta la data nel formato 'yyyy-mm-dd' per il campo input
            const maxDate = twelveYearsAgo.toISOString().split('T')[0];

            // Imposta l'attributo max dell'input date
            dataInput.setAttribute('max', maxDate);
        });

//controllo password
document.getElementById('registrazioneForm').addEventListener('submit', function(event) {
            const password = document.getElementById('password').value;

            // Condizioni da verificare
            const conditions = [
                { regex: /[a-z]/, message: "Almeno una lettera minuscola." },
                { regex: /[A-Z]/, message: "Almeno una lettera maiuscola." },
                { regex: /\d/, message: "Almeno un numero." },
                { regex: /[^\w\s]/, message: "Almeno un carattere speciale." },
                { regex: /^.{8,20}$/, message: "Lunghezza tra 8 e 20 caratteri." }
            ];

            // Raccoglie i messaggi di errore
            let errorMessages = [];
            conditions.forEach(condition => {
                if (!condition.regex.test(password)) {
                    errorMessages.push(condition.message);
                }
            });

            // Se ci sono condizioni non soddisfatte, mostra il pop-up e blocca l'invio
            if (errorMessages.length > 0) {
                event.preventDefault(); // Blocca l'invio del modulo
                alert("Condizioni non soddisfatte:\n\n" + errorMessages.join("\n"));
            }
        });
// Funzione per rendere la prima lettera maiuscola nei campi nome, cognome e SDA
        function capitalizeFirstLetter(element) {
            element.value = element.value.charAt(0).toUpperCase() + element.value.slice(1).toLowerCase();
        }

        // Event listener per i campi nome, cognome e SDA
        document.getElementById('nome').addEventListener('input', function() {
            capitalizeFirstLetter(this);
        });
        document.getElementById('cognome').addEventListener('input', function() {
            capitalizeFirstLetter(this);
        });
        document.getElementById('sda').addEventListener('input', function() {
            capitalizeFirstLetter(this);
        });

        // Event listener per il campo Codice Fiscale (CF) - tutto maiuscolo
        document.getElementById('cf').addEventListener('input', function() {
            // Trasforma il testo in maiuscolo
            this.value = this.value.toUpperCase();

            // Limita la lunghezza massima a 16 caratteri
            if (this.value.length > 16) {
                this.value = this.value.slice(0, 16);
            }
        });

//campo codice univoco disattivato
document.addEventListener("DOMContentLoaded", () => {
    const switchToggle = document.getElementById("pricing-plan-switch"); // Lo switch toggle
    const cu = document.querySelector("input[name='cu'][placeholder='Inserisci il tuo Codice Univoco']"); // Campo Codice Univoco

    // Funzione per mostrare/nascondere il campo
    function toggleCodiceUnivoco() {
        if (switchToggle.checked) {
            // Mostra il campo "Codice Univoco" se lo switch è disattivo
            cu.style.display = "block";
            cu.required = true;
        } else {
            // Nascondi il campo "Codice Univoco" se lo switch è attivo
            cu.style.display = "none";
            cu.value = "";
             cu.required = false;// Cancella il valore per evitare invii non validi
        }
    }

    // Assegna la funzione all'evento 'change' dello switch
    switchToggle.addEventListener("change", toggleCodiceUnivoco);

    // Esegui il controllo iniziale per impostare lo stato corretto
    toggleCodiceUnivoco();
});

window.onload = function() {
    // Verifica se l'URL contiene il parametro "error=password"
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('error') === 'password') {
        // Mostra il pop-up
        alert("Credenziali errate. Riprova.");
    }
    if (urlParams.get('error') === 'formatoEmail') {
        alert("Il formato dell'email è errato. Riprova.");
    }
    else if (urlParams.get('error') === 'formatoNome') {
        alert("Il formato del nome è errato. Riprova.");
    }
    else if (urlParams.get('error') === 'formatoCognome') {
        alert("Il formato del cognome è errato. Riprova.");
    }
    else if (urlParams.get('error') === 'formatoSDA') {
        alert("Il formato del codice SDA è errato. Riprova.");
    }
    else if (urlParams.get('error') === 'formatocf') {
        alert("Il formato del codice fiscale è errato. Riprova.");
    }
    else if (urlParams.get('error') === 'formatoDataNascita') {
        alert("Il formato della data di nascita è errato. Riprova.");
    }
    else if (urlParams.get('error') === 'formatoPassword') {
        alert("Il formato della password è errato. Riprova.");
    }
    else if (urlParams.get('error') === 'formatoCU') {
        alert("Il formato del codice univoco è errato. Riprova.");
    }
    else if (urlParams.get('error') === 'AlreadyRegistered') {
        alert("Utente già registrato. Riprova.");
    }

};


