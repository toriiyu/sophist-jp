# Sophist.jp - 哲学メディア

A modern, clean Japanese philosophy media platform built with static HTML, CSS, and JavaScript. Deploys seamlessly to Cloudflare Pages via GitHub.

## Features

- **Clean, Modern Design**: Medium-style layout with white background and excellent typography
- **Responsive**: Mobile-first design that works on all devices
- **Dark Mode**: Built-in dark mode toggle with localStorage persistence
- **Search Functionality**: Client-side article search
- **Category Filtering**: Browse articles by philosophical category
- **SEO Optimized**: Full meta tags, Open Graph, Twitter Cards, and Schema.org markup
- **Accessibility**: WCAG compliant with proper semantic HTML
- **Performance**: Static HTML generates at build time, no server needed
- **Automatic Deployment**: GitHub Actions workflow for one-click deployments

## Project Structure

```
sophist-jp/
├── index.html                 # Homepage (auto-generated)
├── articles/                  # Individual article pages (auto-generated)
│   └── 001-socrates-intro.html
├── articles_md/               # Source markdown files
│   └── 001-socrates-intro.md
├── templates/                 # HTML templates
│   ├── index_template.html
│   └── article_template.html
├── css/
│   └── style.css             # Main stylesheet
├── js/
│   └── script.js             # Client-side functionality
├── convert_articles.py        # Build script
├── requirements.txt
├── wrangler.toml             # Cloudflare Pages config
├── robots.txt                 # Auto-generated
├── sitemap.xml               # Auto-generated
└── articles.json             # Metadata index (auto-generated)
```

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- GitHub account (for deployment)
- Cloudflare account (for hosting)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/sophist-jp.git
   cd sophist-jp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate static site**
   ```bash
   python convert_articles.py
   ```

4. **Serve locally**
   ```bash
   # Using Python's built-in server
   python -m http.server 8000

   # Or using any static server like http-server
   # npm install -g http-server
   # http-server .
   ```

5. **Open in browser**
   - Navigate to `http://localhost:8000`

## Writing Articles

### Article Format

Articles are written in Markdown with YAML frontmatter. Create files in `articles_md/` directory:

```markdown
---
title: Article Title
category: 第1部：哲学入門
difficulty: 2
keywords: keyword1, keyword2, keyword3
excerpt: A brief summary of the article (shown in listings)
date: 2024-03-15
---

## Section Heading

Article content in markdown format...

### Subsection

More content with **bold** and *italic* text.
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `title` | Yes | Article title (displayed prominently) |
| `category` | Yes | One of the 6 predefined categories |
| `difficulty` | Yes | Integer 1-5 (displayed as stars) |
| `keywords` | Yes | Comma-separated SEO keywords |
| `excerpt` | Yes | Brief summary for article listings |
| `date` | No | ISO 8601 format (defaults to build time) |

### Category Options

- `第1部：哲学入門` - Introduction to Philosophy
- `第2部：古代哲学` - Ancient Philosophy
- `第3部：中世哲学` - Medieval Philosophy
- `第4部：近代哲学` - Modern Philosophy
- `第5部：現代哲学（20世紀）` - Contemporary Philosophy (20th Century)
- `第6部：21世紀の哲学` - 21st Century Philosophy

### Supported Markdown Features

- Headers (`# ## ###`)
- Bold, italic, strikethrough
- Lists (ordered and unordered)
- Code blocks with syntax highlighting
- Tables
- Blockquotes
- Links and images
- Footnotes

## Building & Deployment

### Local Build

```bash
python convert_articles.py
```

This generates:
- `index.html` - Homepage with article listings
- `articles/*.html` - Individual article pages
- `sitemap.xml` - XML sitemap for search engines
- `robots.txt` - Robots directive
- `articles.json` - Metadata index

### Deploy to Cloudflare Pages

#### Setup (One-time)

1. **Create Cloudflare Account**
   - Go to https://dash.cloudflare.com
   - Create a new account

2. **Create Pages Project**
   - In Cloudflare dashboard: Pages > Create a project
   - Select "Connect to Git"
   - Authorize GitHub and select `sophist-jp` repository
   - Framework preset: "None"
   - Build command: `pip install -r requirements.txt && python convert_articles.py`
   - Build output directory: `.`

3. **Set Environment Variables**
   - Create GitHub secrets in your repository:
     - `CLOUDFLARE_API_TOKEN`: Get from Cloudflare dashboard > Account > API Tokens
     - `CLOUDFLARE_ACCOUNT_ID`: Get from Cloudflare dashboard > Account

4. **Enable GitHub Actions**
   - Workflows should auto-run on push to `main`

#### Deployment Workflow

1. Create article(s) in `articles_md/` directory
2. Commit and push to `main` branch
3. GitHub Actions automatically:
   - Installs dependencies
   - Runs `convert_articles.py`
   - Deploys to Cloudflare Pages
4. Site is live at `sophist-jp.pages.dev` (or your custom domain)

### Custom Domain

1. In Cloudflare dashboard: Pages > Settings > Custom domains
2. Add your domain (e.g., `sophist.jp`)
3. Update nameservers at your registrar to point to Cloudflare

## Design Features

### Color Scheme

| Purpose | Color | CSS Variable |
|---------|-------|--------------|
| Background | White/Dark | `--primary-bg` |
| Text | Dark Gray/Light Gray | `--primary-text` |
| Accent | Blue | `--accent-color` |
| Categories | 6 distinct colors | `--category-1` through `--category-6` |

### Typography

- **Font**: Noto Sans JP (Google Fonts)
- **Body**: 16px, 1.8 line-height
- **Headings**: Semantic sizes (h1-h6)
- **Code**: Courier New, monospace

### Responsive Breakpoints

- **Desktop**: 1200px max content width
- **Tablet**: 768px breakpoint
- **Mobile**: 480px breakpoint

## JavaScript Features

### Dark Mode
- Toggleable with button in header
- Persists preference to localStorage
- Respects system preference on first visit

### Search
- Real-time article filtering
- Searches title, excerpt, and category
- Shows "no results" message when appropriate

### Category Filter
- Toggle filter buttons
- Displays matching articles only
- "All" button resets filters

### Table of Contents
- Auto-generated from H2 and H3 headings
- Sticky sidebar on desktop
- Smooth scroll navigation
- Hidden if no headings exist

### Additional Features
- Reading time estimation
- Lazy loading support (for future image optimization)
- Code block copy button
- Keyboard navigation (arrow keys)
- Share buttons (Twitter, Facebook, LINE, link copy)

## Performance Optimizations

- **Static Generation**: All HTML pre-rendered at build time
- **No Database**: Zero server load required
- **CDN Delivery**: Served globally via Cloudflare
- **Minimal CSS**: Optimized stylesheet (~10KB)
- **Minimal JS**: No heavy frameworks (~8KB)
- **No Analytics Overhead**: Optional analytics without bloat

## SEO

### Built-in SEO Features

- Full meta descriptions
- Open Graph tags for social sharing
- Twitter Card support
- Schema.org JSON-LD structured data
- XML sitemap generation
- robots.txt with sitemap reference
- Canonical URLs
- Semantic HTML5 markup

### SEO Checklist

- [ ] Add custom favicon (`favicon.svg`)
- [ ] Update footer copyright and license
- [ ] Configure custom domain
- [ ] Submit sitemap to Google Search Console
- [ ] Add site verification to Cloudflare
- [ ] Monitor Core Web Vitals in Cloudflare Analytics

## Configuration

### Customize Styling

Edit `css/style.css` to modify:
- Color scheme (CSS variables at top)
- Typography (fonts, sizes)
- Layout (widths, spacing)
- Dark mode colors

### Customize Functionality

Edit `js/script.js` to modify:
- Reading time calculation (words per minute)
- Share button platforms
- Search behavior
- Animation durations

### Customize Templates

Edit template files in `templates/`:
- `index_template.html` - Homepage structure
- `article_template.html` - Article page structure

## Troubleshooting

### Articles not appearing
- Ensure markdown files are in `articles_md/` directory
- Check YAML frontmatter is valid (use YAML validator online)
- Run `python convert_articles.py` and check for errors

### Deployment fails
- Check GitHub Actions logs in repository
- Ensure all secrets are set correctly
- Verify `requirements.txt` dependencies are installed
- Check that Cloudflare credentials are valid

### Styling looks wrong
- Clear browser cache (Ctrl+Shift+Delete)
- Check CSS file is loading (DevTools > Network)
- Verify no CSS conflicts with extensions

### Dark mode not working
- Check localStorage isn't blocked
- Verify `js/script.js` is loading
- Check browser console for errors

## Advanced Usage

### Custom Build Hook

Modify `convert_articles.py` to:
- Add custom metadata processing
- Implement advanced templating
- Generate additional file types
- Add pre/post-build steps

### Content Analysis

Access `articles.json` for:
- Article metrics
- Category distributions
- Date range analysis
- SEO keyword analysis

## License

This template is provided as-is. Content articles should use appropriate licenses (CC-BY 4.0 recommended).

## Support

For issues or questions:
1. Check GitHub issues
2. Verify setup against local build instructions
3. Review Cloudflare Pages documentation
4. Check browser console for errors

## Future Enhancements

Potential additions (not included in this version):
- Comment system (via external service)
- Author pages
- Related articles widget
- Email subscription
- Social media timeline
- Full-text search engine
- Analytics dashboard
- Automatic social media posting

---

**Built with ❤️ for philosophy enthusiasts**
