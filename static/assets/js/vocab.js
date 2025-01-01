document.addEventListener('DOMContentLoaded', () => {
    fetchData();
    setupEventListeners();
});

let vocabData = [];  // Initialize as an array

function fetchData() {
    // Fetching from Django View
    fetch('/final_data.json')
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
    const flashcard = document.getElementById('flashcard');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const random = document.getElementById('random');
    let israndom = random.checked;
    let currentIndex = 0;

    random.addEventListener('change', () => {
        israndom = random.checked;
    });

    flashcard.addEventListener('click', () => {
        flashcard.classList.toggle('flipped');
    });

    prevBtn.addEventListener('click', () => {
        if (!israndom) {
            if (currentIndex > 0) {
                currentIndex--;
                displayFlashcard(currentIndex);
            } else {
                alert('This is the first flashcard.');
            }
        }
    });

    nextBtn.addEventListener('click', () => {
        if (!israndom) {
            if (currentIndex < vocabData.length - 1) {
                currentIndex++;
                displayFlashcard(currentIndex);
            } else {
                alert('You have reached the last flashcard.');
            }
        } else {
            currentIndex = Math.floor(Math.random() * vocabData.length);
            displayFlashcard(currentIndex);
        }
    });
}

function displayFlashcard(index) {
    const front = document.getElementById('front');
    const back = document.getElementById('back');

    console.log(`Displaying flashcard at index: ${index}`);

    if (!vocabData || vocabData.length === 0) {
        front.textContent = 'No vocabulary data available.';
        back.textContent = '';
        return;
    }

    if (index < 0 || index >= vocabData.length) {
        front.textContent = 'Index out of bounds.';
        back.textContent = '';
        return;
    }

    const vocab = vocabData[index];
    console.log(`Current Word: ${vocab.word}, Part of Speech: ${vocab.partOfSpeech}`);
    front.textContent = `${vocab.word} (${vocab.partOfSpeech})`;
    back.textContent = vocab.definition;

    // Ensure the card is not flipped when displaying a new card
    const flashcard = document.getElementById('flashcard');
    flashcard.classList.remove('flipped');
}