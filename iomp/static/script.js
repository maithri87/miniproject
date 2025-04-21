async function loadGenres() {
    let genreSelect = document.getElementById("genreSelect");

    try {
        let response = await fetch("/genres");
        let genres = await response.json();

        genreSelect.innerHTML = "<option value=''>Select Genre</option>";
        genres.forEach(genre => {
            let option = document.createElement("option");
            option.value = genre;
            option.textContent = genre;
            genreSelect.appendChild(option);
        });
    } catch (error) {
        console.error("Error loading genres:", error);
    }
}

async function filterSongs() {
    let mood = document.getElementById("moodSelect").value;
    let genre = document.getElementById("genreSelect").value;

    try {
        let response = await fetch(`/filter?mood=${encodeURIComponent(mood)}&genre=${encodeURIComponent(genre)}`);
        let data = await response.json();

        let resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = "";

        if (data.length === 0) {
            resultsDiv.innerHTML = "<p>No songs found for the selected criteria.</p>";
            return;
        }

        data.forEach(song => {
            let songElement = document.createElement("div");
            songElement.className = "song-card";
            songElement.innerHTML = `
                <p class="song-title">${song.name}</p>
                <p>Genre: ${song.genres}</p>
                <p>Mood: ${song.mood}</p>
                <p>Popularity: ${song.popularity}</p>
            `;
            resultsDiv.appendChild(songElement);
        });
    } catch (error) {
        console.error("Error fetching filtered songs:", error);
    }
}

async function getRecommendations() {
    let songInput = document.getElementById("songInput");
    let moodSelect = document.getElementById("moodSelect");
    let genreSelect = document.getElementById("genreSelect");

    let songName = songInput ? songInput.value : "";
    let mood = moodSelect ? moodSelect.value : "";
    let genre = genreSelect ? genreSelect.value : "";

    try {
        let response = await fetch(`/recommend?song=${encodeURIComponent(songName)}&mood=${encodeURIComponent(mood)}&genre=${encodeURIComponent(genre)}`);
        let data = await response.json();

        let resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = "";

        if (data.error) {
            resultsDiv.innerHTML = `<p>${data.error}</p>`;
            return;
        }

        if (data.length === 0) {
            resultsDiv.innerHTML = "<p>No recommendations found. Try different filters.</p>";
            return;
        }

        data.forEach(song => {
            let songElement = document.createElement("div");
            songElement.className = "song-card";
            songElement.innerHTML = `
                <p class="song-title"><strong>${song.name}</strong></p>
                <p>Genre: ${song.genres}</p>
                <p>Mood: ${song.mood}</p>
                <p>Popularity: ${song.popularity}</p>
            `;
            resultsDiv.appendChild(songElement);
        });
    } catch (error) {
        console.error("Error fetching recommendations:", error);
    }
}

function clearFilters() {
    document.getElementById("moodSelect").value = "";
    document.getElementById("genreSelect").value = "";
    let songInput = document.getElementById("songInput");
    if (songInput) songInput.value = "";

    let resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "<p>Filters cleared! Select options to see songs.</p>";
}

window.onload = loadGenres;
