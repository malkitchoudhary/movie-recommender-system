const API_URL = "/recommend";


const movieInput = document.getElementById("movieName");
const dropdownButton = document.getElementById("dropdownButton");
const dropdownList = document.getElementById("dropdownList");
const recommendButton = document.getElementById("recommendButton");
const message = document.getElementById("message");
const results = document.getElementById("results");

const movieOptions = [
  "Avatar",
  "Spider-Man 3",
  "Spider-Man 2",
  "Spider-Man",
  "The Amazing Spider-Man",
  "The Amazing Spider-Man 2",
  "The Dark Knight",
  "Batman Begins",
  "Batman Returns",
  "Batman Forever",
  "Batman & Robin",
  "Iron Man",
  "Iron Man 2",
  "Iron Man 3",
  "The Avengers",
  "Avengers: Age of Ultron",
  "Titanic",
  "Interstellar",
  "Inception",
  "The Matrix",
  "Joker",
  "Superman Returns",
  "Man of Steel",
  "Deadpool",
  "Thor",
  "Captain America: The First Avenger",
  "Guardians of the Galaxy",
];

const defaultMovies = [
  {
    title: "Spider-Man 2",
    poster_url: "https://image.tmdb.org/t/p/w500/olxpyq9kJAZ2NU1siLshhhXEPR7.jpg",
  },
  {
    title: "Spider-Man",
    poster_url: "https://image.tmdb.org/t/p/w500/gh4cZbhZxyTbgxQPxD0dOudNPTn.jpg",
  },
  {
    title: "The Amazing Spider-Man",
    poster_url: "https://image.tmdb.org/t/p/w500/jexoNYnPd6vVrmygwF6QZmWPFdu.jpg",
  },
  {
    title: "The Dark Knight",
    poster_url: "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
  },
  {
    title: "Iron Man",
    poster_url: "https://image.tmdb.org/t/p/w500/78lPtwv72eTNqFW9COBYI0dWDJa.jpg",
  },
];

function showMessage(text) {
  message.textContent = text;
}

function showMovies(movies) {
  results.innerHTML = "";

  movies.forEach((movie) => {
    const card = document.createElement("div");
    card.className = "movie-card";

    const title = document.createElement("h3");
    title.textContent = movie.title;

    const poster = document.createElement("img");
    poster.src = movie.poster_url;
    poster.alt = movie.title;

    poster.onerror = function () {
      poster.src = "https://via.placeholder.com/500x750/252631/ffffff?text=No+Poster";
    };

    card.appendChild(title);
    card.appendChild(poster);
    results.appendChild(card);
  });
}

function renderDropdown(filterText = "") {
  const searchText = filterText.trim().toLowerCase();

  const filteredMovies = movieOptions.filter((movie) =>
    movie.toLowerCase().includes(searchText)
  );

  dropdownList.innerHTML = "";

  if (filteredMovies.length === 0) {
    const emptyItem = document.createElement("div");
    emptyItem.className = "dropdown-item";
    emptyItem.textContent = "No movie found";
    dropdownList.appendChild(emptyItem);
    dropdownList.classList.add("show");
    return;
  }

  filteredMovies.forEach((movie) => {
    const item = document.createElement("div");
    item.className = "dropdown-item";
    item.textContent = movie;

    item.addEventListener("click", function () {
      movieInput.value = movie;
      dropdownList.classList.remove("show");
      movieInput.focus();
    });

    dropdownList.appendChild(item);
  });

  dropdownList.classList.add("show");
}

function hideDropdown() {
  setTimeout(function () {
    dropdownList.classList.remove("show");
  }, 180);
}

async function recommendMovie() {
  const movieName = movieInput.value.trim();

  if (!movieName) {
    showMessage("Please enter or select a movie name.");
    return;
  }

  recommendButton.disabled = true;
  recommendButton.textContent = "Loading...";
  dropdownList.classList.remove("show");
  showMessage("Finding recommendations...");

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        movie_name: movieName,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Something went wrong.");
    }

    showMovies(data.recommendations);
    showMessage("");
  } catch (error) {
    showMessage(error.message);
  } finally {
    recommendButton.disabled = false;
    recommendButton.textContent = "Recommend";
  }
}

movieInput.addEventListener("focus", function () {
  renderDropdown(movieInput.value);
});

movieInput.addEventListener("input", function () {
  renderDropdown(movieInput.value);
});

movieInput.addEventListener("blur", hideDropdown);

dropdownButton.addEventListener("click", function () {
  if (dropdownList.classList.contains("show")) {
    dropdownList.classList.remove("show");
  } else {
    renderDropdown(movieInput.value);
    movieInput.focus();
  }
});

recommendButton.addEventListener("click", recommendMovie);

movieInput.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    recommendMovie();
  }
});

showMovies(defaultMovies);
showMessage("");
