document.addEventListener('DOMContentLoaded', () => {
    const showFormButton = document.getElementById('show-form-button');
    const profileForm = document.querySelector('.profileform');
    const loginForm = document.querySelector('#login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault(); // Prevents the default form submission
            const formData = new FormData(loginForm);
            fetch('/login?next=/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest', 
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('login-message');
                messageDiv.innerHTML = `
                          <div class="login-message">
                            <strong>Success!</strong><br>
                            <p>Login successful. Welcome!</p>
                            <button class="close-btn" onclick="this.parentElement.remove()">×</button> <!-- Close button -->
                        </div>`; 
                // Appends the message div to the body or any other element on the page
                document.body.appendChild(messageDiv);
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 3000);
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error during login:', error);
            });
        });
    }
    showFormButton.addEventListener('click', () => {
        showFormButton.style.display = 'none'; 
        profileForm.style.display = 'block'; 
    });
    
    // Hide form and show button after form submission
    profileForm.addEventListener('submit', () => {
        setTimeout(() => {
            profileForm.style.display = 'none'; 
            showFormButton.style.display = 'block'; 
        }, 100);
    });

    
    
});

 
// searchInput.addEventListener('input', () => {
//     const query = searchInput.value;
//     if (!query.trim()) {
//         return; // Do nothing if the query is empty
//     }

//     urlElements.forEach(urlElement => {
//         const url = urlElement.getAttribute('data-url'); 
        
//         // Example: Log the URL for each module
//         console.log('Module URL:', url);

//          if (!url) {
//             console.error('URL attribute is missing for this element!');
//             return;
//         }

//     // Use the URL and append the query parameter
//     fetch(`${url}?q=${encodeURIComponent(query)}`, {
//         method: 'GET',
//         headers: {
//             'X-Requested-With': 'XMLHttpRequest',  // Add this header explicitly
//         }
//     })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }
//         return response.json();
//     })
//     .then(data => {
//         if (data.html) {
//             moduleTableBody.innerHTML = data.html; // Update the table body with the results
//         }
//     })
//     .catch(error => {
//         console.error('Error fetching data:', error);
//     });
// });
// });