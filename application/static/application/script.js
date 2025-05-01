document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('btnCommentairesFiltres');
    const fenetre = document.getElementById('commentairesFiltres');
    
    btn.addEventListener('click', function() {
        if (fenetre.style.display === 'none') {
            fenetre.style.display = 'block';
            btn.style.display = 'none';
        }
    });
});