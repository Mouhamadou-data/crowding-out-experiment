let currentGrid = [];
let submittedWords = [];
let timeRemaining = 0;
let timerInterval = null;
let hiddenFieldName = '';

function initializePuzzle(gridPhase, duration, fieldName) {
    hiddenFieldName = fieldName;
    timeRemaining = duration;
    submittedWords = [];
    fetch('/static/word_grids.json')
        .then(function(r) { return r.ok ? r.json() : Promise.reject('Not found'); })
        .then(function(data) {
            if (data.grids && data.grids[gridPhase]) {
                currentGrid = data.grids[gridPhase];
                renderPuzzle();
                startTimer();
            } else { alert('Grid not found.'); }
        })
        .catch(function(e) { console.error(e); alert('Error loading puzzle.'); });
}

function renderPuzzle() {
    var html = '<div class="timer-section"><div id="timer-display">Time: ' + formatTime(timeRemaining) + '</div></div>';
    html += '<div class="grid-container" style="text-align:center;">' + renderGrid() + '</div>';
    html += '<div class="word-input-section">';
    html += '<input type="text" id="word-input" placeholder="Type a word and press Enter" autocomplete="off" autofocus>';
    html += '<div id="feedback-message"></div></div>';
    html += '<div class="submitted-words-section">';
    html += '<div id="word-count-display">Words Found: <span id="word-count">0</span></div>';
    html += '<ul id="submitted-words-list"></ul></div>';
    document.getElementById('puzzle-container').innerHTML = html;
    document.getElementById('word-input').addEventListener('keypress', handleKeyPress);
    document.getElementById('word-input').focus();
}

function renderGrid() {
    var html = '';
    for (var i = 0; i < currentGrid.length; i++) {
        html += '<div class="grid-row">';
        for (var j = 0; j < currentGrid[i].length; j++) {
            html += '<div class="grid-cell">' + currentGrid[i][j] + '</div>';
        }
        html += '</div>';
    }
    return html;
}

function handleKeyPress(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        var word = e.target.value.trim().toUpperCase();
        if (word.length > 0) {
            processWord(word);
            e.target.value = '';
        }
    }
}

function processWord(word) {
    if (word.length < 4) {
        showFeedback('Min 4 letters', 'error');
        return;
    }
    if (submittedWords.indexOf(word) !== -1) {
        showFeedback('Already submitted', 'error');
        return;
    }
    submittedWords.push(word);
    updateWordsList();
    saveWordsToHiddenField();
    showFeedback('Word added!', 'success');
}

function saveWordsToHiddenField() {
    var f = document.querySelector('input[name="' + hiddenFieldName + '"]');
    if (f) {
        f.value = JSON.stringify(submittedWords);
        console.log('Saved:', f.value);
    }
}

function showFeedback(msg, type) {
    var d = document.getElementById('feedback-message');
    if (d) {
        d.textContent = msg;
        d.className = 'feedback-' + type;
        setTimeout(function() { d.textContent = ''; d.className = ''; }, 2000);
    }
}

function updateWordsList() {
    document.getElementById('word-count').textContent = submittedWords.length;
    var ul = document.getElementById('submitted-words-list');
    ul.innerHTML = '';
    for (var i = 0; i < submittedWords.length; i++) {
        var li = document.createElement('li');
        li.className = 'word-badge';
        li.textContent = submittedWords[i];
        ul.appendChild(li);
    }
}

function startTimer() {
    updateTimerDisplay();
    timerInterval = setInterval(function() {
        timeRemaining--;
        updateTimerDisplay();
        if (timeRemaining <= 0) endPuzzle();
    }, 1000);
}

function updateTimerDisplay() {
    var d = document.getElementById('timer-display');
    if (d) {
        d.textContent = 'Time: ' + formatTime(timeRemaining);
        if (timeRemaining <= 30) {
            d.style.backgroundColor = '#f8d7da';
            d.style.color = '#721c24';
        } else if (timeRemaining <= 60) {
            d.style.backgroundColor = '#fff3cd';
            d.style.color = '#856404';
        }
    }
}

function formatTime(s) {
    var mins = Math.floor(s / 60);
    var secs = s % 60;
    return mins + ':' + (secs < 10 ? '0' : '') + secs;
}

function endPuzzle() {
    clearInterval(timerInterval);
    var inp = document.getElementById('word-input');
    if (inp) {
        inp.disabled = true;
        inp.placeholder = 'Time is up!';
    }
    saveWordsToHiddenField();
    setTimeout(function() {
        var form = document.querySelector('form');
        if (form) form.submit();
    }, 2000);
}

window.addEventListener('beforeunload', saveWordsToHiddenField);
setInterval(function() { if (submittedWords.length > 0) saveWordsToHiddenField(); }, 5000);