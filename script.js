const url = "http://localhost:5001/music"; // change endpoint

window.addEventListener("load", () => fetchMusic());

function reload() {
  window.location.reload();
}

async function fetchMusic(query = "") {
  try {
    const res = await fetch(url);
    const data = await res.json();

    let musicList = data.music || [];

    // 🔍 Search filter
    if (query) {
      const searchQuery = query.toLowerCase();

      musicList = musicList.filter(song =>
        song.title?.toLowerCase().includes(searchQuery) ||
        song.artist?.toLowerCase().includes(searchQuery) ||
        song.album?.toLowerCase().includes(searchQuery) ||
        song.genre?.toLowerCase().includes(searchQuery)
      );
    }

    bindData(musicList);
  } catch (error) {
    console.error("Error fetching music:", error);
  }
}

function bindData(musicList) {
  const cardsContainer = document.getElementById("cards-container");
  const musicCardTemplate = document.getElementById("template-music-card");

  cardsContainer.innerHTML = "";

  if (musicList.length === 0) {
    cardsContainer.innerHTML = `<h2>No music found 🎵</h2>`;
    return;
  }

  musicList.forEach(song => {
    const cardClone = musicCardTemplate.content.cloneNode(true);
    fillDataInCard(cardClone, song);
    cardsContainer.appendChild(cardClone);
  });
}

function fillDataInCard(cardClone, song) {
  const musicImg = cardClone.querySelector("#music-image");
  const musicTitle = cardClone.querySelector("#music-title");
  const creatorName = cardClone.querySelector("#creator-name");
  const albumName = cardClone.querySelector("#album-name");

  musicImg.src = song.image || "https://via.placeholder.com/400x200";
  musicTitle.innerHTML = song.title || "No title";
  creatorName.innerHTML = song.artist || "Unknown artist";
  albumName.innerHTML = song.album || "Unknown album";

  // 🔥 Click to play / open link
  cardClone.firstElementChild.addEventListener("click", () => {
    if (song.url) {
      window.open(song.url, "_blank");
    }
  });
}