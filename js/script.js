/**
 * Sophist.jp - JavaScript functionality
 * Handles dark mode toggle, search, and UI interactions
 */

// ===== Dark Mode Toggle =====
function initDarkMode() {
  const toggleButton = document.querySelector('.dark-toggle');
  const html = document.documentElement;

  // Load saved preference
  const savedMode = localStorage.getItem('darkMode');
  if (savedMode === 'true') {
    html.classList.add('dark-mode');
    updateToggleIcon();
  } else if (savedMode === null && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    // Use system preference if no saved preference
    html.classList.add('dark-mode');
    updateToggleIcon();
  }

  if (toggleButton) {
    toggleButton.addEventListener('click', function() {
      html.classList.toggle('dark-mode');
      const isDarkMode = html.classList.contains('dark-mode');
      localStorage.setItem('darkMode', isDarkMode);
      updateToggleIcon();
    });
  }
}

function updateToggleIcon() {
  const html = document.documentElement;
  const toggleButton = document.querySelector('.dark-toggle');
  if (toggleButton) {
    toggleButton.textContent = html.classList.contains('dark-mode') ? '☀️' : '🌙';
  }
}

// ===== Search Functionality =====
function initSearch() {
  const searchInput = document.querySelector('.search-box input');
  if (!searchInput) return;

  searchInput.addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const cards = document.querySelectorAll('.article-card');

    cards.forEach(card => {
      const title = card.querySelector('.article-title').textContent.toLowerCase();
      const excerpt = card.querySelector('.article-excerpt').textContent.toLowerCase();
      const category = card.querySelector('.category-badge').textContent.toLowerCase();

      const matches = title.includes(searchTerm) ||
                     excerpt.includes(searchTerm) ||
                     category.includes(searchTerm);

      card.style.display = matches ? '' : 'none';
    });

    // Show "no results" message if needed
    updateSearchResults();
  });
}

function updateSearchResults() {
  const cards = document.querySelectorAll('.article-card');
  const visibleCards = Array.from(cards).filter(card => card.style.display !== 'none');

  // Remove existing "no results" message
  const existingMessage = document.querySelector('.no-results');
  if (existingMessage) {
    existingMessage.remove();
  }

  // Add "no results" message if needed
  if (visibleCards.length === 0 && cards.length > 0) {
    const container = document.querySelector('.articles-grid');
    if (container) {
      const message = document.createElement('div');
      message.className = 'no-results';
      message.textContent = '検索結果がありません';
      message.style.cssText = 'grid-column: 1 / -1; text-align: center; padding: 2rem; color: var(--secondary-text);';
      container.appendChild(message);
    }
  }
}

// ===== Category Filter =====
function initCategoryFilter() {
  const buttons = document.querySelectorAll('.category-filter button');

  buttons.forEach(button => {
    button.addEventListener('click', function() {
      const selectedCategory = this.getAttribute('data-category');
      const isActive = this.classList.contains('active');

      if (selectedCategory === 'all') {
        // Reset all filters
        buttons.forEach(btn => btn.classList.remove('active'));
        this.classList.add('active');
        showAllArticles();
      } else {
        // Toggle the clicked button
        buttons.forEach(btn => {
          if (btn.getAttribute('data-category') === 'all') {
            btn.classList.remove('active');
          }
        });

        if (isActive) {
          this.classList.remove('active');
          showAllArticles();
        } else {
          this.classList.add('active');
          // Remove active from other category buttons
          buttons.forEach(btn => {
            if (btn !== this && btn.getAttribute('data-category') !== 'all') {
              btn.classList.remove('active');
            }
          });
          filterByCategory(selectedCategory);
        }
      }
    });
  });
}

function filterByCategory(category) {
  const cards = document.querySelectorAll('.article-card');
  cards.forEach(card => {
    const cardCategory = card.getAttribute('data-category');
    card.style.display = cardCategory === category ? '' : 'none';
  });
}

function showAllArticles() {
  const cards = document.querySelectorAll('.article-card');
  cards.forEach(card => {
    card.style.display = '';
  });
}

// ===== Table of Contents Generation =====
function initTableOfContents() {
  const toc = document.querySelector('.article-toc ul');
  if (!toc) return;

  const headings = document.querySelectorAll('.article-content h2, .article-content h3');

  headings.forEach((heading, index) => {
    // Add id if not present
    if (!heading.id) {
      heading.id = `heading-${index}`;
    }

    // Create TOC entry
    const li = document.createElement('li');
    li.className = heading.tagName === 'H2' ? 'toc-level-2' : 'toc-level-3';

    const a = document.createElement('a');
    a.href = `#${heading.id}`;
    a.textContent = heading.textContent;

    li.appendChild(a);
    toc.appendChild(li);
  });
}

// ===== Smooth Scroll for TOC Links =====
function initSmoothScroll() {
  document.querySelectorAll('.article-toc a').forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href').substring(1);
      const target = document.getElementById(targetId);
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
}

// ===== Share Buttons =====
function initShareButtons() {
  const shareButtons = document.querySelectorAll('.share-button');

  shareButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();

      const platform = this.getAttribute('data-platform');
      const title = document.querySelector('.article-title-main')?.textContent || 'Sophist.jp';
      const url = window.location.href;

      let shareUrl = '';

      switch(platform) {
        case 'twitter':
          shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(title)}&url=${encodeURIComponent(url)}`;
          break;
        case 'facebook':
          shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
          break;
        case 'line':
          shareUrl = `https://line.me/R/msg/text/?${encodeURIComponent(title + '\n' + url)}`;
          break;
        case 'copy':
          navigator.clipboard.writeText(url).then(() => {
            const originalText = this.textContent;
            this.textContent = 'コピーしました';
            setTimeout(() => {
              this.textContent = originalText;
            }, 2000);
          });
          return;
      }

      if (shareUrl) {
        window.open(shareUrl, '_blank', 'width=600,height=400');
      }
    });
  });
}

// ===== Reading Time Calculation =====
function calculateReadingTime() {
  const content = document.querySelector('.article-content');
  if (!content) return;

  const text = content.textContent;
  const wordCount = text.length;
  const wordsPerMinute = 400; // Average reading speed in Japanese
  const readingTime = Math.ceil(wordCount / wordsPerMinute);

  const readtimeElement = document.querySelector('[data-readtime]');
  if (readtimeElement) {
    readtimeElement.textContent = `${readingTime}分`;
  }
}

// ===== Lazy Loading Images =====
function initLazyLoading() {
  if ('IntersectionObserver' in window) {
    const images = document.querySelectorAll('.article-content img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.getAttribute('data-src');
          img.removeAttribute('data-src');
          observer.unobserve(img);
        }
      });
    });

    images.forEach(img => imageObserver.observe(img));
  }
}

// ===== Navigation Between Articles =====
function initArticleNavigation() {
  const prevLink = document.querySelector('.article-nav .nav-link.prev');
  const nextLink = document.querySelector('.article-nav .nav-link.next');

  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowLeft' && prevLink) {
      window.location.href = prevLink.href;
    } else if (e.key === 'ArrowRight' && nextLink) {
      window.location.href = nextLink.href;
    }
  });
}

// ===== Copy Code Blocks =====
function initCodeCopy() {
  const codeBlocks = document.querySelectorAll('pre');

  codeBlocks.forEach(block => {
    const button = document.createElement('button');
    button.className = 'code-copy-btn';
    button.textContent = 'コピー';
    button.style.cssText = `
      position: absolute;
      right: 10px;
      top: 10px;
      padding: 0.4rem 0.8rem;
      background-color: var(--accent-color);
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 0.8em;
      font-family: 'Noto Sans JP', sans-serif;
    `;

    block.style.position = 'relative';
    block.appendChild(button);

    button.addEventListener('click', function() {
      const code = block.querySelector('code').textContent;
      navigator.clipboard.writeText(code).then(() => {
        const originalText = button.textContent;
        button.textContent = 'コピー完了！';
        setTimeout(() => {
          button.textContent = originalText;
        }, 2000);
      });
    });
  });
}

// ===== Initialization =====
document.addEventListener('DOMContentLoaded', function() {
  initDarkMode();
  initSearch();
  initCategoryFilter();
  initTableOfContents();
  initSmoothScroll();
  initShareButtons();
  initArticleNavigation();
  calculateReadingTime();
  initLazyLoading();
  initCodeCopy();
});

// ===== Service Worker Registration (Optional) =====
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    // Uncomment to enable service worker for offline support
    // navigator.serviceWorker.register('/sw.js');
  });
}
