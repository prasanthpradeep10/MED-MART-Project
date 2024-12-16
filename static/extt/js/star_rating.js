document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = '{{ csrf_token }}';  // Make sure this is present in your HTML template

    document.querySelectorAll('.star-rating .star').forEach(function(star) {
        star.addEventListener('click', function() {
            const value = this.getAttribute('data-value');
            const parent = this.closest('.star-rating');
            const productId = parent.getAttribute('data-product-id');

            // Update star display
            parent.querySelectorAll('.star').forEach(function(s) {
                s.innerHTML = '&#9734;';  // Empty star
            });
            for (let i = 0; i < value; i++) {
                parent.querySelectorAll('.star')[i].innerHTML = '&#9733;';  // Filled star
            }

            // Send rating to backend via AJAX
            fetch('/rate-product/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `product_id=${productId}&rating=${value}`,
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                // Optionally update average rating on the page
            });
        });
    });
});
