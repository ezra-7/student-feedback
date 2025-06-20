function validateForm() {
    const rating = document.querySelector('input[name="rating"]').value;
    if (rating < 1 || rating > 5) {
        alert("Rating must be between 1 and 5");
        return false;
    }
    return true;
}
