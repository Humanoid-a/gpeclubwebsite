
const set_path = params.set_path;
const set_name = params.set_name;
var israndom = false;
let modeUnknown = false;
let Index = 0;

//alert(set_path);


document.addEventListener('DOMContentLoaded', () => {
    fetchData();
    setupEventListeners();
    const progress = document.getElementById(`progress`);
    const progressInfo = document.getElementById(`progressInfo`);
    const progressBar = document.querySelector('.progress-bar');
    let percentage = Math.round((knownWords.length / vocabData.length) * 100);
    progress.innerText = percentage.toString() + '%';
    progressBar.style.width = percentage.toString() + '%';
    progressInfo.innerText = 'Progress: ' + knownWords.length.toString() + '/' + vocabData.length.toString();
});
hideSpinner();
let knownWords = [];
let unknownWords = [];
let viewed = [0];
let order = 0;
let previous = 0;
let isIdk = false;

if (getCookieSingle('previous') !== null) {
    previous = getCookieSingle('previous');
    console.log(previous);
}
let currentIndex = previous;

let vocabData = [];  // Initialize as an array
if (getCookie('knownWordsAI') !== null) {
    let knownWordsCookie = getCookie('knownWordsAI');
    knownWords = knownWordsCookie ? JSON.parse(knownWordsCookie) : [];
    if (!Array.isArray(knownWords)) {
        knownWords = [];
    }
} else {
    knownWords = [];
}
console.log(knownWords);
if (getCookie('unknownWordsAI') !== null) {
    let unknownWordsCookie = getCookie('unknownWordsAI');
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

function setCookieSingle(name, value) {
    const cookieName = `${name}_${set_name}`;
    document.cookie = cookieName + "=" + value.toString() + "; path=/";
}
function getCookieSingle(name) {
    const cookieName = `${name}_${set_name}`;
    const nameEQ = cookieName + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i].trim();
        if (c.indexOf(nameEQ) === 0) return parseInt(c.substring(nameEQ.length, c.length), 10);
    }
    return null;
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
                displayFlashcard(currentIndex);
            } else {
                console.warn('vocabData is empty.');
                displayFlashcard(currentIndex);
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
    const next = document.getElementById('next');
    const prev = document.getElementById('prev');
    const idk = document.getElementById('idk');

    modeUnknown = practiceUnknown.checked;
    israndom = random.checked;
    let unknownIndex = 0;
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
        setCookieSingle('previous', 0);
        getNum();
    });
    prev.addEventListener('click', () => {
        const response = document.getElementById(`response-0`);
        const def = document.getElementById(`response-2`);
        response.innerText = '';
        def.innerText = '';
        if (order > 0){
            currentIndex = viewed[order];
            order -= 1;
            displayFlashcard(currentIndex);
        }
        displayFlashcard(currentIndex);
        console.log(order);
    });
    next.addEventListener('click', () => {
        isIdk = false;
        const response = document.getElementById(`response-0`);
        const def = document.getElementById(`response-2`);
        response.innerText = '';
        def.innerText = '';
        order += 1;
        if(!modeUnknown){
            viewed[order] = currentIndex;
            if (!israndom){
                currentIndex++;
                if (knownWords !== null) {
                    while (knownWords.includes(currentIndex)) {
                        currentIndex++;
                    }
                }
            }else{
                currentIndex = Math.floor(Math.random() * vocabData.length);
                if (knownWords !== null) {
                    while (knownWords.includes(currentIndex)) {
                        currentIndex = Math.floor(Math.random() * vocabData.length);
                    }
                }
            }
            displayFlashcard(currentIndex);
        }else{
            viewed[order] = unknownWords[Index];
            if (!israndom){
                if(Index < unknownWords.length - 1) {
                    Index++;
                }else{
                    Index = 0;
                }
            }else{
                Index = Math.floor(Math.random() * unknownWords.length);
                while(unknownWords[Index] === viewed[order]){
                    Index = Math.floor(Math.random() * unknownWords.length);
                }
            }
            displayFlashcard(unknownWords[Index]);
        }

    });
    idk.addEventListener('click', () => {
        isIdk = true;
        const response = document.getElementById(`response-0`);
        const def = document.getElementById(`response-2`);
        response.innerText = 'Pass';
        def.innerText = vocabData[currentIndex].definition;
        unknownWords.push(currentIndex);
        unknownWords = [...new Set(unknownWords)];
        console.log(unknownWords);
        getNum()
        setCookie('unknownWordsAI', JSON.stringify(unknownWords));
        displayProgress();
    })
}
function showSpinner() {
  document.getElementById('spinner').style.display = 'flex';
}

function hideSpinner() {
  document.getElementById('spinner').style.display = 'none';
}
async function AI(text, index) {
    const vocab = vocabData[index];
    const developer = 'You are given a vocabulary and its definition and Chinese translation below. Determine if the user\'s input generally and broadly matches the idea or Chinese translation of the vocabulary term. Answer with only "Correct" or "Incorrect".';
    const def = `${vocab.word}: ${vocab.definition}`;
    const prompt = `${developer} ${def}`;
    const input = text;
    const response = document.getElementById(`response-0`);
    response.innerText = '';
    showSpinner()

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
        displayDefinition(index);

        if (response.ok) {
            console.log('AI Response:', data.response);
            // Update your UI with the AI response
            displayAIResponse(index, data.response);
        } else {
            console.error('Backend Error:', data.error);
            // Optionally, display an error message to the user
            displayAIError(index, data.error);
        }
        hideSpinner()
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

function displayProgress(){
    const progress = document.getElementById(`progress`);
    const progressInfo = document.getElementById(`progressInfo`);
    const progressBar = document.querySelector('.progress-bar');
    let percentage = Math.round((knownWords.length / vocabData.length) * 100);
    progress.innerText = percentage.toString() + '%';
    progressBar.style.width = percentage.toString() + '%';
    progressInfo.innerText = 'Progress: ' + knownWords.length.toString() + '/' + vocabData.length.toString() + ' words known';
    return;
}

// Function to display AI response in the UI
function displayAIResponse(index, response) {
    const responseElement = document.getElementById(`response-0`);
    responseElement.innerText = response;
    if (response === 'Correct') {
        if(!modeUnknown){
            knownWords.push(currentIndex);
            unknownWords = unknownWords.filter(item => item !== currentIndex);
        }else{
            knownWords.push(unknownWords[Index]);
            unknownWords = unknownWords.filter(item => item !== unknownWords[Index]);
        }
        knownWords = [...new Set(knownWords)];
        setCookie('knownWordsAI', JSON.stringify(knownWords));
    }else{
        if(!modeUnknown) {
            unknownWords.push(currentIndex);
        }
        unknownWords = [...new Set(unknownWords)];
        setCookie('unknownWordsAI', JSON.stringify(unknownWords));
    }
    getNum();
}

function displayDefinition(index) {
    const responseElement = document.getElementById(`response-2`);
    responseElement.innerText = 'Definition: ' + vocabData[index].definition;
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
        if (text === '' && !isIdk) {
            console.warn('No text entered.');
            displayAIResponse(currentIndex, 'Please enter a definition or translation.');
            return;
        }
        if(modeUnknown){
            AI(text, unknownWords[Index]);
        }else{
            AI(text, currentIndex);
        }
        textInput.value = ''; // Optionally, clear the input field
    });
});




function displayFlashcard(index) {
    displayProgress()
    const front = document.getElementById('front');
    previous = currentIndex;
        console.log(previous);
         setCookieSingle('previous', previous);

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