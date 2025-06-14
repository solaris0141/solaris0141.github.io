const calendarSVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler-calendar-week"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M4 7a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2v-12z"/><path d="M16 3v4"/><path d="M8 3v4"/><path d="M4 11h16"/><path d="M7 14h.013"/><path d="M10.01 14h.005"/><path d="M13.01 14h.005"/><path d="M16.015 14h.005"/><path d="M13.015 17h.005"/><path d="M7.01 17h.005"/><path d="M10.01 17h.005"/></svg>`;
const postsPerPage = 9;
let currentPage = 1;
const featuredPost = blogPosts[0];
const otherPosts   = blogPosts.slice(1);
const totalPages   = Math.ceil(otherPosts.length / postsPerPage);

function renderFeatured(post) {
  document.getElementById("featured-post").innerHTML = `
    <div class="featured-text">
      <span class="featured-tag">latest ${post.type}</span>
      <div class="featured-date-row">
        <span class="icon">${calendarSVG}</span>
        <small>${post.date}</small>
      </div>
      <h2 class="featured-title">
        <a href="${post.link}">${post.title}</a>
      </h2>
      <a class="featured-button" href="${post.link}">Read</a>
    </div>
    <div class="featured-image">
      <div class="image-crop-3-2">
        <img src="${post.image}" alt="${post.title}">
      </div>
    </div>
  `;
}


function renderBlogList(posts) {
  const listEl = document.getElementById("blog-list");
  listEl.innerHTML = posts.map(post => `
    <div class="blog-card">
      <img src="${post.image}" alt="${post.title}" />
      <div class="blog-card-inner">
        <div class="date-row">
          <span class="icon">${calendarSVG}</span>
          <small>${post.date}</small>
          <span class="post-type">${post.type}</span>
        </div>
        <h3 class="post-title">
          <a href="${post.link}">${post.title}</a>
        </h3>
      </div>
    </div>
  `).join("");
}

function paginatePosts() {
  const start = (currentPage - 1) * postsPerPage;
  const pageItems = otherPosts.slice(start, start + postsPerPage);
  renderBlogList(pageItems);
}

function renderPagination() {
  const container = document.getElementById("pagination-controls");
  container.innerHTML = "";

  // — “Newest” button → jump to page 1
  const newestBtn = document.createElement('button');
  newestBtn.textContent = 'Newest';
  newestBtn.disabled = (currentPage === 1);
  newestBtn.addEventListener('click', () => {
    currentPage = 1;
    paginatePosts();
    renderPagination();
  });
  container.appendChild(newestBtn);

  // — compute sliding window of up to 9 pages, centered around currentPage
  const maxButtons = 9;
  const half       = Math.floor(maxButtons / 2); // 4
  let startPage, endPage;

  if (totalPages <= maxButtons) {
    startPage = 1;
    endPage   = totalPages;
  } else {
    if (currentPage <= half + 1) {
      // near the start
      startPage = 1;
      endPage   = maxButtons;
    } else if (currentPage + half >= totalPages) {
      // near the end
      endPage   = totalPages;
      startPage = totalPages - maxButtons + 1;
    } else {
      // centered window
      startPage = currentPage - half;
      endPage   = currentPage + half;
    }
  }

  // — numbered page buttons
  for (let i = startPage; i <= endPage; i++) {
    const btn = document.createElement('button');
    btn.textContent = i;
    if (i === currentPage) btn.classList.add('active');
    btn.addEventListener('click', () => {
      currentPage = i;
      paginatePosts();
      renderPagination();
    });
    container.appendChild(btn);
  }

  // — “Oldest” button → jump to last page
  const oldestBtn = document.createElement('button');
  oldestBtn.textContent = 'Oldest';
  oldestBtn.disabled = (currentPage === totalPages);
  oldestBtn.addEventListener('click', () => {
    currentPage = totalPages;
    paginatePosts();
    renderPagination();
  });
  container.appendChild(oldestBtn);
}

document.addEventListener("DOMContentLoaded", () => {
  renderFeatured(featuredPost);
  paginatePosts();
  renderPagination();
});