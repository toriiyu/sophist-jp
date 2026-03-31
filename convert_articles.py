#!/usr/bin/env python3
"""
Sophist.jp Article Converter
Converts Markdown articles with YAML frontmatter to HTML pages.
"""

import os
import sys
import re
import json
import yaml
import markdown
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from urllib.parse import quote


class ArticleConverter:
    """Convert markdown articles to HTML pages."""

    CATEGORIES = {
        '第1部：哲学入門': 'intro',
        '第2部：古代哲学': 'ancient',
        '第3部：中世哲学': 'medieval',
        '第4部：近代哲学': 'modern',
        '第5部：現代哲学（20世紀）': 'contemporary',
        '第6部：21世紀の哲学': 'future',
    }

    CATEGORY_COLORS = {
        'intro': '--category-1',
        'ancient': '--category-2',
        'medieval': '--category-3',
        'modern': '--category-4',
        'contemporary': '--category-5',
        'future': '--category-6',
    }

    def __init__(self, base_path: str = '.'):
        """Initialize converter with base path."""
        self.base_path = Path(base_path)
        self.articles_md_dir = self.base_path / 'articles_md'
        self.articles_dir = self.base_path / 'articles'
        self.templates_dir = self.base_path / 'templates'
        self.articles = []

    def read_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """Extract YAML frontmatter and markdown content."""
        # Match YAML frontmatter between --- delimiters
        match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)

        if not match:
            raise ValueError("Article must start with YAML frontmatter delimited by ---")

        try:
            frontmatter = yaml.safe_load(match.group(1))
            markdown_content = match.group(2)
            return frontmatter, markdown_content
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML frontmatter: {e}")

    def markdown_to_html(self, markdown_content: str) -> str:
        """Convert markdown to HTML with extensions."""
        md = markdown.Markdown(
            extensions=[
                'tables',
                'fenced_code',
                'codehilite',
                'toc',
                'nl2br',
                'md_in_html',
            ],
            extension_configs={
                'codehilite': {'css_class': 'highlight'},
                'toc': {'permalink': False, 'baselevel': 2},
            }
        )

        html = md.convert(markdown_content)
        return html

    def generate_difficulty_stars(self, difficulty: int) -> str:
        """Generate HTML for difficulty stars."""
        max_stars = 5
        filled = min(max(difficulty, 0), max_stars)
        empty = max_stars - filled

        stars = ''.join(['<span class="star filled">★</span>' for _ in range(filled)])
        stars += ''.join(['<span class="star">☆</span>' for _ in range(empty)])

        return stars

    def generate_share_buttons(self) -> str:
        """Generate HTML for share buttons."""
        return '''<div class="article-share">
    <a href="#" class="share-button" data-platform="twitter" title="Twitterで共有">𝕏</a>
    <a href="#" class="share-button" data-platform="facebook" title="Facebookで共有">f</a>
    <a href="#" class="share-button" data-platform="line" title="LINEで共有">LINE</a>
    <button class="share-button" data-platform="copy" title="リンクをコピー">🔗</button>
  </div>'''

    def generate_toc_html(self, markdown_content: str) -> str:
        """Generate table of contents HTML."""
        # Extract headings from markdown
        headings = re.findall(r'^(#{2,3})\s+(.+)$', markdown_content, re.MULTILINE)

        if not headings:
            return '<aside class="article-toc" style="display:none;"><h4>目次</h4><ul></ul></aside>'

        # Build TOC HTML
        toc_html = '<aside class="article-toc"><h4>目次</h4><ul>'

        for heading_level, heading_text in headings:
            level = len(heading_level)
            toc_level = f'toc-level-{level}'
            # Create valid ID from heading text
            sanitized_text = re.sub(r"[^\w]", "-", heading_text.lower())
            heading_id = f'heading-{sanitized_text}'

            toc_html += f'<li class="{toc_level}"><a href="#{heading_id}">{heading_text}</a></li>'

        toc_html += '</ul></aside>'
        return toc_html

    def generate_article_nav(self, current_idx: int, total_articles: int) -> str:
        """Generate next/previous article navigation."""
        if total_articles <= 1:
            return ''

        nav_html = '<nav class="article-nav">'

        if current_idx > 0:
            prev_title = self.articles[current_idx - 1].get('title', '前の記事')
            prev_slug = self.articles[current_idx - 1].get('slug', 'index')
            nav_html += f'''<a href="/articles/{prev_slug}.html" class="nav-link prev">
      <span class="nav-link-label">← 前の記事</span>
      <span class="nav-link-title">{prev_title}</span>
    </a>'''
        else:
            nav_html += '<div></div>'

        if current_idx < total_articles - 1:
            next_title = self.articles[current_idx + 1].get('title', '次の記事')
            next_slug = self.articles[current_idx + 1].get('slug', 'index')
            nav_html += f'''<a href="/articles/{next_slug}.html" class="nav-link next">
      <span class="nav-link-label">次の記事 →</span>
      <span class="nav-link-title">{next_title}</span>
    </a>'''
        else:
            nav_html += '<div></div>'

        nav_html += '</nav>'
        return nav_html

    def process_article(self, filepath: Path) -> Dict:
        """Process a single markdown article."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        try:
            frontmatter, markdown_content = self.read_frontmatter(content)
        except ValueError as e:
            print(f"Error processing {filepath}: {e}", file=sys.stderr)
            return None

        # Validate required fields
        required_fields = ['title', 'category', 'difficulty', 'excerpt']
        for field in required_fields:
            if field not in frontmatter:
                print(f"Warning: {filepath} missing '{field}' in frontmatter", file=sys.stderr)

        # Generate slug from filename
        slug = filepath.stem

        # Convert markdown to HTML
        html_content = self.markdown_to_html(markdown_content)

        # Generate difficulty stars
        difficulty = frontmatter.get('difficulty', 1)
        difficulty_html = self.generate_difficulty_stars(difficulty)

        # Prepare article metadata
        date_value = frontmatter.get('date', datetime.now().isoformat())
        # Ensure date is a string
        if not isinstance(date_value, str):
            date_value = date_value.isoformat()

        article = {
            'slug': slug,
            'title': frontmatter.get('title', 'Untitled'),
            'category': frontmatter.get('category', '未分類'),
            'category_key': self.get_category_key(frontmatter.get('category', '')),
            'difficulty': difficulty,
            'difficulty_html': difficulty_html,
            'excerpt': frontmatter.get('excerpt', ''),
            'keywords': frontmatter.get('keywords', ''),
            'content': html_content,
            'markdown': markdown_content,
            'date': date_value,
        }

        return article

    def get_category_key(self, category: str) -> str:
        """Get category key for styling."""
        for cat_name, cat_key in self.CATEGORIES.items():
            if category.startswith(cat_key) or cat_name == category:
                return cat_key
        return 'intro'

    def generate_article_html(self, article: Dict, article_idx: int, total_articles: int) -> str:
        """Generate HTML for a single article page."""
        with open(self.templates_dir / 'article_template.html', 'r', encoding='utf-8') as f:
            template = f.read()

        # Generate components
        difficulty_stars = self.generate_difficulty_stars(article['difficulty'])
        share_buttons = self.generate_share_buttons()
        article_nav = self.generate_article_nav(article_idx, total_articles)

        # Replace placeholders
        html = template.replace('{{title}}', article['title'])
        html = html.replace('{{excerpt}}', article['excerpt'])
        html = html.replace('{{keywords}}', article['keywords'])
        html = html.replace('{{url}}', f"https://sophist.jp/articles/{article['slug']}.html")
        html = html.replace('{{date}}', article['date'])
        html = html.replace('{{category}}', article['category'])
        html = html.replace('{{difficulty_stars}}', difficulty_stars)
        html = html.replace('{{content}}', article['content'])
        html = html.replace('{{share_buttons}}', share_buttons)
        html = html.replace('{{article_nav}}', article_nav)

        # Remove unused TOC if no headings
        if '<h2' not in article['content'] and '<h3' not in article['content']:
            html = re.sub(
                r'<aside class="article-toc".*?</aside>',
                '',
                html,
                flags=re.DOTALL
            )

        return html

    def generate_article_card(self, article: Dict) -> str:
        """Generate HTML card for article listing."""
        reading_time = max(1, len(article['content']) // 400)

        return f'''<article class="article-card" data-category="{article['category_key']}">
    <a href="/articles/{article['slug']}.html">
      <div class="article-meta">
        <span class="category-badge">{article['category']}</span>
        <div class="difficulty-stars">
          {article['difficulty_html']}
        </div>
      </div>
      <h2 class="article-title">{article['title']}</h2>
      <p class="article-excerpt">{article['excerpt']}</p>
      <span class="article-readtime">{reading_time}分で読める</span>
    </a>
  </article>'''

    def generate_category_buttons(self) -> str:
        """Generate HTML for category filter buttons."""
        buttons = []
        for category_name, category_key in self.CATEGORIES.items():
            buttons.append(f'<button data-category="{category_key}">{category_name}</button>')
        return '\n      '.join(buttons)

    def generate_index_html(self) -> str:
        """Generate index page HTML."""
        with open(self.templates_dir / 'index_template.html', 'r', encoding='utf-8') as f:
            template = f.read()

        # Generate article cards
        article_cards = '\n  '.join([
            self.generate_article_card(article) for article in self.articles
        ])

        # Generate category buttons
        category_buttons = self.generate_category_buttons()

        # Replace placeholders
        html = template.replace('{{articles}}', article_cards)
        html = html.replace('{{category_buttons}}', category_buttons)

        return html

    def convert_all(self) -> Tuple[int, int]:
        """Convert all articles and generate index."""
        if not self.articles_md_dir.exists():
            print(f"Error: {self.articles_md_dir} does not exist", file=sys.stderr)
            return 0, 0

        # Create output directories
        self.articles_dir.mkdir(exist_ok=True)

        # Process all markdown files
        md_files = sorted(self.articles_md_dir.glob('*.md'))

        if not md_files:
            print(f"Warning: No markdown files found in {self.articles_md_dir}", file=sys.stderr)

        for md_file in md_files:
            article = self.process_article(md_file)
            if article:
                self.articles.append(article)
            else:
                print(f"Skipped: {md_file}", file=sys.stderr)

        # Sort articles by date (newest first)
        self.articles.sort(key=lambda x: x['date'], reverse=True)

        # Generate article HTML files
        for idx, article in enumerate(self.articles):
            html = self.generate_article_html(article, idx, len(self.articles))
            output_file = self.articles_dir / f"{article['slug']}.html"

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)

            print(f"Generated: {output_file}")

        # Generate index HTML
        index_html = self.generate_index_html()
        index_file = self.base_path / 'index.html'

        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_html)

        print(f"Generated: {index_file}")

        return len(self.articles), len(md_files)

    def generate_sitemap(self) -> str:
        """Generate XML sitemap."""
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

        # Homepage
        sitemap += '  <url>\n'
        sitemap += '    <loc>https://sophist.jp/</loc>\n'
        sitemap += f'    <lastmod>{datetime.now().isoformat()}</lastmod>\n'
        sitemap += '    <changefreq>daily</changefreq>\n'
        sitemap += '    <priority>1.0</priority>\n'
        sitemap += '  </url>\n'

        # Articles
        for article in self.articles:
            sitemap += '  <url>\n'
            sitemap += f'    <loc>https://sophist.jp/articles/{article["slug"]}.html</loc>\n'
            sitemap += f'    <lastmod>{article["date"]}</lastmod>\n'
            sitemap += '    <changefreq>monthly</changefreq>\n'
            sitemap += '    <priority>0.8</priority>\n'
            sitemap += '  </url>\n'

        sitemap += '</urlset>'
        return sitemap

    def generate_robots_txt(self) -> str:
        """Generate robots.txt."""
        return '''User-agent: *
Allow: /
Disallow: /admin/

Sitemap: https://sophist.jp/sitemap.xml
'''

    def save_metadata(self):
        """Save articles metadata to JSON for reference."""
        metadata = []
        for article in self.articles:
            metadata.append({
                'slug': article['slug'],
                'title': article['title'],
                'category': article['category'],
                'difficulty': article['difficulty'],
                'date': article['date'],
                'excerpt': article['excerpt'],
            })

        metadata_file = self.base_path / 'articles.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        print(f"Saved metadata to: {metadata_file}")


def main():
    """Main entry point."""
    base_path = os.path.dirname(os.path.abspath(__file__)) if len(sys.argv) == 1 else sys.argv[1]

    converter = ArticleConverter(base_path)

    print(f"Converting articles from {converter.articles_md_dir}...")
    successful, total = converter.convert_all()

    if successful == 0:
        print("No articles were converted. Make sure to add .md files to articles_md/")
        return 1

    print(f"\nConversion complete! {successful}/{total} articles processed.")

    # Generate additional files
    sitemap = converter.generate_sitemap()
    sitemap_file = converter.base_path / 'sitemap.xml'
    with open(sitemap_file, 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print(f"Generated: {sitemap_file}")

    robots = converter.generate_robots_txt()
    robots_file = converter.base_path / 'robots.txt'
    with open(robots_file, 'w', encoding='utf-8') as f:
        f.write(robots)
    print(f"Generated: {robots_file}")

    # Save metadata
    converter.save_metadata()

    return 0


if __name__ == '__main__':
    sys.exit(main())
