const postsPerPage = 6;
let currentPage = 1;
const heroPost = blogPosts.length > 0 ? blogPosts[0] : null;
const archivePosts = blogPosts.length > 1 ? blogPosts.slice(1) : [];
const totalPages = Math.ceil(archivePosts.length / postsPerPage);

function renderHero() {
    const heroContainer = document.getElementById("hero-section");
    
    if (!heroPost) {
        heroContainer.innerHTML = `<div style="padding:2rem; color:white;">NO_DATA_AVAILABLE</div>`;
        return;
    }

    heroContainer.innerHTML = `
        <div class="hero-text-side">
            <div>
                <span class="hero-label">LATEST_POST</span>
                <h1 class="hero-title">${heroPost.title}</h1>
                <div class="font-mono" style="color: var(--c-slate); font-size: 0.8rem; margin-bottom: 1rem;">
                    DATE: ${heroPost.date} // ${heroPost.type.toUpperCase()}
                </div>
            </div>
            <a href="${heroPost.link}" class="read-more-btn">
                READ_MORE ->
            </a>
        </div>
        <div class="hero-visual-side">
            <img src="${heroPost.image}" class="hero-img" alt="${heroPost.title}">
            <div class="hero-overlay"></div>
            <div class="absolute" style="bottom: 1rem; right: 1rem; border: 1px solid var(--c-beige); padding: 0.5rem; color: var(--c-beige); font-family: var(--font-mono); font-size: 0.7rem;">
                IMG_REF: ${heroPost.type.toUpperCase()}_01
            </div>
        </div>
    `;
}

function renderGrid() {
    const gridContainer = document.getElementById("blog-grid");
    gridContainer.innerHTML = "";

    const start = (currentPage - 1) * postsPerPage;
    const end = start + postsPerPage;
    const pageItems = archivePosts.slice(start, end);

    if (pageItems.length === 0) {
        gridContainer.innerHTML = `<div style="color:var(--c-slate);">NO_ARCHIVES_FOUND</div>`;
        return;
    }

    const gridHTML = pageItems.map(post => {
        return `
        <a href="${post.link}" class="blog-card">
            <div class="card-img-container">
                <img src="${post.image}" class="card-img" alt="${post.title}">
            </div>
            <div class="card-content">
                <div>
                    <div class="card-meta">${post.date} // ${post.type.toUpperCase()}</div>
                    <h3 class="card-title">${post.title}</h3>
                </div>
                <div class="card-arrow">ACCESS_POST -></div>
            </div>
        </a>
        `;
    }).join("");

    gridContainer.innerHTML = gridHTML;
}

function renderPagination() {
    const container = document.getElementById("pagination-container");
    container.innerHTML = "";

    const infoDiv = document.createElement("div");
    infoDiv.className = "pagination-info";
    infoDiv.innerText = `PAGE ${currentPage} OF ${totalPages} // TOTAL_POSTS: ${blogPosts.length}`;
    container.appendChild(infoDiv);

    const btnContainer = document.createElement("div");
    btnContainer.className = "pagination-buttons";

    const prevBtn = document.createElement("a");
    prevBtn.href = "#";
    prevBtn.className = `page-link ${currentPage === 1 ? 'disabled' : ''}`;
    prevBtn.innerText = "< PREV";
    prevBtn.addEventListener("click", (e) => {
        e.preventDefault();
        if (currentPage > 1) {
            currentPage--;
            updateDisplay();
        }
    });
    btnContainer.appendChild(prevBtn);

    const addPageBtn = (pageNum) => {
        const btn = document.createElement("a");
        btn.href = "#";
        btn.className = `page-link ${pageNum === currentPage ? 'active' : ''}`;
        btn.innerText = pageNum;
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            currentPage = pageNum;
            updateDisplay();
        });
        btnContainer.appendChild(btn);
    };

    const addEllipsis = () => {
        const span = document.createElement("span");
        span.style.fontFamily = "var(--font-mono)";
        span.style.color = "var(--c-slate)";
        span.style.alignSelf = "center";
        span.innerText = "...";
        btnContainer.appendChild(span);
    };

    const maxVisible = 5;

    if (totalPages <= maxVisible) {
        for (let i = 1; i <= totalPages; i++) {
            addPageBtn(i);
        }
    } else {
        addPageBtn(1);

        let startPage = Math.max(2, currentPage - 1);
        let endPage = Math.min(totalPages - 1, currentPage + 1);

        if (currentPage <= 3) {
            endPage = 4;
        }

        if (currentPage >= totalPages - 2) {
            startPage = totalPages - 3;
        }

        if (startPage > 2) addEllipsis();

        for (let i = startPage; i <= endPage; i++) {
            addPageBtn(i);
        }

        if (endPage < totalPages - 1) addEllipsis();

        addPageBtn(totalPages);
    }

    const nextBtn = document.createElement("a");
    nextBtn.href = "#";
    nextBtn.className = `page-link ${currentPage === totalPages ? 'disabled' : ''}`;
    nextBtn.innerText = "NEXT >";
    nextBtn.addEventListener("click", (e) => {
        e.preventDefault();
        if (currentPage < totalPages) {
            currentPage++;
            updateDisplay();
        }
    });
    btnContainer.appendChild(nextBtn);

    container.appendChild(btnContainer);
}

function updateDisplay() {
    renderHero();
    renderGrid();
    renderPagination();
}

document.addEventListener("DOMContentLoaded", () => {
    updateDisplay();
});