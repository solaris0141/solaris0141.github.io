document.querySelector('.hamburger').addEventListener('click', () => {
  document.querySelector('.nav-links').classList.toggle('show');
});

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

function initHighlights() {
  if (window.hljs) {
    document.querySelectorAll('pre code').forEach(block => {
      hljs.highlightElement(block);
    });
  }
}

function initCopyButtons() {
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const codeEl = btn.closest('.code-block-wrapper').querySelector('pre code');
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

function initExpandableCodeBlocks() {
  const threshold = 70;
  document.querySelectorAll('.code-block-wrapper').forEach(wrapper => {
    const toggle = wrapper.querySelector('.toggle-btn');
    const codeEl = wrapper.querySelector('pre code');
    if (!toggle || !codeEl) return;

    // 1) Count lines in the code
    const lineCount = codeEl.innerText.split('\n').length;

    // 2) Decide initial collapsed state
    const shouldCollapse = lineCount > threshold;
    if (shouldCollapse) {
      wrapper.classList.add('collapsed');
      toggle.innerHTML = expandSvg;
      toggle.setAttribute('aria-label','Expand snippet');
    } else {
      wrapper.classList.remove('collapsed');
      toggle.innerHTML = collapseSvg;
      toggle.setAttribute('aria-label','Collapse snippet');
    }

    // 3) Hook up click to toggle
    toggle.addEventListener('click', () => {
      const collapsed = wrapper.classList.toggle('collapsed');
      toggle.innerHTML = collapsed ? expandSvg : collapseSvg;
      toggle.setAttribute(
        'aria-label',
        collapsed ? 'Expand snippet' : 'Collapse snippet'
      );
    });
  });
}

const expandSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
viewBox="0 0 24 24" fill="currentColor"
class="icon icon-tabler icons-tabler-filled icon-tabler-caret-right">
<path stroke="none" d="M0 0h24v24H0z" fill="none"/>
<path d="M9 6c0 -.852 .986 -1.297 1.623 -.783l.084 .076l6 6a1 1 0 0 1 .083 1.32l-.083 .094l-6 6l-.094 .083l-.077 .054l-.096 .054l-.036 .017l-.067 .027l-.108 .032l-.053 .01l-.06 .01l-.057 .004l-.059 .002l-.059 -.002l-.058 -.005l-.06 -.009l-.052 -.01l-.108 -.032l-.067 -.027l-.132 -.07l-.09 -.065l-.081 -.073l-.083 -.094l-.054 -.077l-.054 -.096l-.017 -.036l-.027 -.067l-.032 -.108l-.01 -.053l-.01 -.06l-.004 -.057l-.002 -12.059z" />
</svg>`;
const collapseSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
viewBox="0 0 24 24" fill="currentColor"
class="icon icon-tabler icons-tabler-filled icon-tabler-caret-down">
<path stroke="none" d="M0 0h24v24H0z" fill="none"/>
<path d="M18 9c.852 0 1.297 .986 .783 1.623l-.076 .084l-6 6a1 1 0 0 1 -1.32 .083l-.094 -.083l-6 -6l-.083 -.094l-.054 -.077l-.054 -.096l-.017 -.036l-.027 -.067l-.032 -.108l-.01 -.053l-.01 -.06l-.004 -.057v-.118l.005 -.058l.009 -.06l.01 -.052l.032 -.108l.027 -.067l.07 -.132l.065 -.09l.073 -.081l.094 -.083l.077 -.054l.096 -.054l.036 -.017l.067 -.027l.108 -.032l.053 -.01l.06 -.01l.057 -.004l12.059 -.002z"/>
</svg>`;

document.addEventListener('DOMContentLoaded', async () => {
  await loadExternalSnippets();
  initHighlights();
  initCopyButtons();
  initExpandableCodeBlocks();



});