
const set_path = params.set_path;
const set_name = params.set_name;
var currentIndex = 0;
var israndom = false;
//alert(set_path);


document.addEventListener('DOMContentLoaded', () => {
    fetchData();
    setupEventListeners();
});


var knownWords = [];
var unknownWords = [];
var viewed = [];

let vocabData = [];  // Initialize as an array
if (getCookie('knownWords') !== null) {
    let knownWordsCookie = getCookie('knownWords');
    knownWords = knownWordsCookie ? JSON.parse(knownWordsCookie) : [];
    if (!Array.isArray(knownWords)) {
        knownWords = [];
    }
} else {
    knownWords = [];
}
console.log(knownWords);
if (getCookie('unknownWords') !== null) {
    let unknownWordsCookie = getCookie('unknownWords');
    unknownWords = unknownWordsCookie ? JSON.parse(unknownWordsCookie) : [];
    if (!Array.isArray(unknownWords)) {
        unknownWords = [];
    }
} else {
    unknownWords = [];
}
console.log(unknownWords);

function setCookie(name, value) {
    const cookieName = `${name}_${set_name}`;
    document.cookie = cookieName + "=" + (value || "") + "; path=/";
}
function getCookie(name) {
    const cookieName = `${name}_${set_name}`;
    const nameEQ = cookieName + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function fetchData() {
    // Fetching from Django View
    fetch(set_path)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Vocabulary Data Loaded:', data); // Debugging statement
            // Convert the dictionary to an array of objects
            for (let word in data) {
                if (data.hasOwnProperty(word)) {
                    data[word].forEach(entry => {
                        vocabData.push({
                            word: word,
                            partOfSpeech: entry[0],
                            definition: entry[1].trim()
                        });
                    });
                }
            }
            console.log('Processed Vocab Data:', vocabData); // Debugging statement
            if (vocabData.length > 0) {
                displayFlashcard(0);
            } else {
                console.warn('vocabData is empty.');
                displayFlashcard(0);
            }
        })
        .catch(error => {
            console.error('Error loading vocabulary data:', error);
            const front = document.getElementById('front');
            front.textContent = 'Error loading vocabulary data.';
        });
}

function setupEventListeners() {
    const random = document.getElementById('random');
    const practiceUnknown = document.getElementById('practiceUnknown');
    const clear = document.getElementById('clear');

    let modeUnknown = practiceUnknown.checked;
    israndom = random.checked;
    let unknownIndex = 0;
    let Index = 0;

    random.addEventListener('change', () => {
        israndom = random.checked;
    });
    practiceUnknown.addEventListener('change', () => {
        modeUnknown = practiceUnknown.checked;
    });

    document.addEventListener('keydown', (event) => {

    });
    clear.addEventListener('click', () => {
        knownWords = [];
        unknownWords = [];
        setCookie('knownWordsAI', JSON.stringify(knownWords));
        setCookie('unknownWordsAI', JSON.stringify(unknownWords));
        getNum();
    });
}

async function AI(text, index) {
    const vocab = vocabData[index];
    const developer = 'You are given a vocabulary and its definition and Chinese translation below. Determine if the user\'s input generally matches the idea or Chinese translation of the vocabulary term. Answer with only "Yes" or "No".';
    const def = `${vocab.word}: ${vocab.definition}`;
    const prompt = `${developer} ${def}`;
    const input = text;

    console.log('Prompt:', prompt);
    console.log('Input:', input);

    try {
        const response = await fetch('/en/api/get-openai-response/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(), // Function to retrieve CSRF token
            },
            body: JSON.stringify({
                prompt: prompt,
                input: input,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            console.log('AI Response:', data.response);
            // Update your UI with the AI response
            displayAIResponse(index, data.response);
        } else {
            console.error('Backend Error:', data.error);
            // Optionally, display an error message to the user
            displayAIError(index, data.error);
        }
    } catch (error) {
        console.error('Network or Server Error:', error);
        // Optionally, display a network error message to the user
        displayAIError(index, 'A network error occurred. Please try again.');
    }
}

// Function to retrieve CSRF token from cookies
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

// Function to display AI response in the UI
function displayAIResponse(index, response) {
    const responseElement = document.getElementById(`response-0`);
    responseElement.innerText = response;
    displayFlashcard(currentIndex);
    if (response === 'Yes') {
        knownWords.push(vocabData[currentIndex].word);
        setCookie('knownWordsAI', JSON.stringify(knownWords));
    }else{
        unknownWords.push(vocabData[currentIndex].word);
        setCookie('unknownWordsAI', JSON.stringify(unknownWords));
    }
    getNum();
}

// Function to display AI error in the UI
function displayAIError(index, errorMessage) {
    const responseElement = document.getElementById(`response-1`);
    if (responseElement) {
        responseElement.innerText = `Error: ${errorMessage}`;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed'); // Debugging log

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
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting the traditional way
        let text = textInput.value.trim();
        console.log('Submitted text:', text);
        if (text === '') {
            console.warn('No text entered.');
            displayAIResponse(currentIndex, 'Please enter a definition or translation.');
            return;
        }
        AI(text, currentIndex);
        if (!israndom){
            currentIndex++;
        }else{
            currentIndex = Math.floor(Math.random() * vocabData.length);
        }
        textInput.value = ''; // Optionally, clear the input field
    });
});




function displayFlashcard(index) {
    const front = document.getElementById('front');

    console.log(`Displaying flashcard at index: ${index}`);

    if (!vocabData || vocabData.length === 0) {
        front.textContent = 'No vocabulary data available.';
        return;
    }

    if (index < 0 || index >= vocabData.length) {
        front.textContent = 'Index out of bounds.';
        return;
    }

    const vocab = vocabData[index];
    console.log(`Current Word: ${vocab.word}, Part of Speech: ${vocab.partOfSpeech}`);
    front.textContent = `${vocab.word} (${vocab.partOfSpeech})`;

    getNum();
    // Ensure the card is not flipped when displaying a new card
}

function getNum(){
    const numKnown = document.getElementById('numKnown');
    const numUnknown = document.getElementById('numUnknown');
    numKnown.textContent = 'Known words count: ' + knownWords.length.toString();
    numUnknown.textContent = 'Unknown words count: ' + unknownWords.length.toString();
}