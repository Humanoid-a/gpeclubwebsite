// Utility function to retrieve CSRF token
function getCsrfToken() {
    let cookieValue = null;
    const name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to call your AI backend
async function AI(text) {
    // Show the box if it's hidden
    const responseBox = document.getElementById('response-0');
    responseBox.style.display = 'block';

    // Show placeholder and hide the actual response text
    const placeholder = document.getElementById('loadingPlaceholder');
    const actualResponse = document.getElementById('actualResponse');
    placeholder.style.display = 'block';
    actualResponse.style.display = 'none';

    try {
        const fetchResponse = await fetch('/en/api/get-openai-response/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({ prompt: text, input: text }),
        });

        const data = await fetchResponse.json();

        if (fetchResponse.ok) {
            // Hide placeholder and show actual response text
            placeholder.style.display = 'none';
            actualResponse.style.display = 'block';
            actualResponse.innerText = data.response;
        } else {
            placeholder.style.display = 'none';
            actualResponse.style.display = 'block';
            actualResponse.innerText = `Error: ${data.error}`;
        }
    } catch (error) {
        placeholder.style.display = 'none';
        actualResponse.style.display = 'block';
        actualResponse.innerText = 'A network error occurred. Please try again.';
    }
}

// Attach event listener when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('textForm');
    const textInput = document.getElementById('textInput');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const text = textInput.value.trim();
        if (text) {
            AI(text);
        }
    });
});


// Function to display AI response in the UI
function displayAIResponse(response) {
    const responseElement = document.getElementById('response-0');
    if (responseElement) {
        responseElement.innerText = response;
    }
}

// Function to display AI error in the UI
function displayAIError(errorMessage) {
    const responseElement = document.getElementById('response-1');
    if (responseElement) {
        responseElement.innerText = `Error: ${errorMessage}`;
    }
}

// Wait for the DOM to be loaded before attaching event listeners
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');

    const form = document.getElementById('textForm');
    const textInput = document.getElementById('textInput');

    if (!form) {
        console.error('Form with id "textForm" not found.');
        return;
    }
    if (!textInput) {
        console.error('Input with id "textInput" not found.');
        return;
    }

    // Attach form submission handler
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        let text = textInput.value.trim();
        console.log('Submitted text:', text);

        if (text === '') {
            console.warn('No text entered.');
            displayAIResponse('Please enter a definition or translation.');
            return;
        }

        // Call AI function
        AI(text);

        // Optionally clear the input field
        textInput.value = '';
    });
});
