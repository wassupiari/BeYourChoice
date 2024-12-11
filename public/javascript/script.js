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
document.addEventListener('DOMContentLoaded', function () {
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
document.getElementById('registrazioneForm').addEventListener('submit', function (event) {
    const password = document.getElementById('password').value;

    // Condizioni da verificare
    const conditions = [
        {regex: /[a-z]/, message: "Almeno una lettera minuscola."},
        {regex: /[A-Z]/, message: "Almeno una lettera maiuscola."},
        {regex: /\d/, message: "Almeno un numero."},
        {regex: /[^\w\s]/, message: "Almeno un carattere speciale."},
        {regex: /^.{8,20}$/, message: "Lunghezza tra 8 e 20 caratteri."}
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
document.getElementById('nome').addEventListener('input', function () {
    capitalizeFirstLetter(this);
});
document.getElementById('cognome').addEventListener('input', function () {
    capitalizeFirstLetter(this);
});
document.getElementById('sda').addEventListener('input', function () {
    capitalizeFirstLetter(this);
});

// Event listener per il campo Codice Fiscale (CF) - tutto maiuscolo
document.getElementById('cf').addEventListener('input', function () {
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


window.onload = function () {
    // Verifica se l'URL contiene il parametro "error"
    const urlParams = new URLSearchParams(window.location.search);
    const errorType = urlParams.get('error');

    if (errorType) {
        // Configurazione delle notifiche Toastr

                toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": true,
        "progressBar": true,
        "positionClass": "toast-bottom-center", // Posiziona in basso al centro
        "preventDuplicates": true,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };




        // Mostra il messaggio in base al tipo di errore
        switch (errorType) {
            case 'password':
                toastr.error("Credenziali errate. Riprova.");
                break;
            case 'formatoEmail':
                toastr.error("Il formato dell'email è errato. Riprova.");
                break;
            case 'formatoNome':
                toastr.error("Il formato del nome è errato. Riprova.");
                break;
            case 'formatoCognome':
                toastr.error("Il formato del cognome è errato. Riprova.");
                break;
            case 'formatoSDA':
                toastr.error("Il formato del codice SDA è errato. Riprova.");
                break;
            case 'formatocf':
                toastr.error("Il formato del codice fiscale è errato. Riprova.");
                break;
            case 'formatoDataNascita':
                toastr.error("Il formato della data di nascita è errato. Riprova.");
                break;
            case 'formatoPassword':
                toastr.error("Il formato della password è errato. Riprova.");
                break;
            case 'formatoCU':
                toastr.error("Il formato del codice univoco è errato. Riprova.");
                break;
            case 'alreadyRegistered':
                toastr.info("Utente già registrato. Reindirizzamento alla pagina di login...");
                // Rimuove il parametro 'error' dalla URL
                const url = new URL(window.location.href);
                url.searchParams.delete('error');
                window.history.replaceState({}, '', url);
                // Reindirizza alla pagina di login
                setTimeout(() => {
                    window.location.replace('/login');
                }, 3000); // Attendi 3 secondi prima del reindirizzamento
                break;
            default:
                toastr.error("Errore sconosciuto. Riprova.");
        }
    }
};



function showPwd() {
    const passwordField = document.getElementById("password");
    const type = passwordField.type === "password" ? "text" : "password";
    passwordField.type = type;

    // Cambia l'icona
    document.getElementById("togglePassword").classList.toggle("fa-eye-slash");
}

function showPwd2() {
    const passwordField = document.getElementById("password2");
    const type = passwordField.type === "password" ? "text" : "password";
    passwordField.type = type;

    // Cambia l'icona
    document.getElementById("togglePassword2").classList.toggle("fa-eye-slash");
}


function showToast(type, message) {
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": true,
        "progressBar": true,
        "positionClass": "toast-bottom-center", // Posiziona in basso al centro
        "preventDuplicates": true,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };

    toastr[type](message);
}
