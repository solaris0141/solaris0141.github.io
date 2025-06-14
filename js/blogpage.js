// 1) Mobile menu toggle
document.querySelector('.hamburger').addEventListener('click', () => {
  document.querySelector('.nav-links').classList.toggle('show');
});

// 2) Load external code snippets
async function loadExternalSnippets() {
  const codeBlocks = document.querySelectorAll('pre code[data-src]');
  await Promise.all(Array.from(codeBlocks).map(async (codeEl) => {
    const url = codeEl.getAttribute('data-src');
    try {
      const resp = await fetch(url);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      codeEl.textContent = (await resp.text()).trim();
    } catch (err) {
      console.error(`Failed to load ${url}:`, err);
      codeEl.textContent = `// ERROR loading ${url}`;
    }
  }));
}

// 3) Initialize Highlight.js on each block
function initHighlights() {
  if (window.hljs) {
    document.querySelectorAll('pre code').forEach(block => {
      hljs.highlightElement(block);
    });
  }
}

// 4) Copy-to-clipboard buttons
function initCopyButtons() {
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const codeEl = btn.closest('.code-block').querySelector('pre code');
      if (!codeEl) return;
      try {
        await navigator.clipboard.writeText(codeEl.innerText);
        btn.classList.add('copied');
        setTimeout(() => btn.classList.remove('copied'), 2000);
      } catch (err) {
        console.error('Copy failed', err);
      }
    });
  });
}

// 5) On DOM ready, wire everything up
document.addEventListener('DOMContentLoaded', async () => {
  await loadExternalSnippets();
  initHighlights();
  initCopyButtons();
});