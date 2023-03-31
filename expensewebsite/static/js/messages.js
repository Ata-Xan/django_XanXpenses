const alert = document.querySelector('.alert');
// Delay the start of the fade-out effect by 5 seconds
setTimeout(() => {
    // Add a CSS transition to the element's opacity property
    alert.style.transition = 'opacity 0.5s';

    // Gradually reduce the element's opacity to 0 over 500 milliseconds
    alert.style.opacity = 0;

    // Set a timeout to remove the element from the DOM after the fade-out effect has finished
    setTimeout(() => {
        alert.remove();
    }, 500);
}, 5000);

document.addEventListener('DOMContentLoaded', function () {
    var confirmDeleteModal = document.getElementById('confirm-delete-modal');
    var deleteBtn = document.querySelectorAll('#delete-btn');
    var cancelButton = confirmDeleteModal.querySelector('.btn-secondary');

    deleteBtn.addEventListener('click', function (e) {
        e.preventDefault();
        var deleteUrl = deleteBtn.getAttribute('href');
        console.log(deleteUrl)
        confirmDeleteModal.querySelector('.modal-footer a').setAttribute('href', deleteUrl);
        confirmDeleteModal.classList.add('show');
    });

    cancelButton.addEventListener('click', function () {
        confirmDeleteModal.classList.remove('show');
    });
});