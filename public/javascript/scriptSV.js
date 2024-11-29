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