# gpeclub/management/commands/build_site_index.py
from django.core.management.base import BaseCommand
from django.urls import URLResolver, URLPattern
import json
import os
from bs4 import BeautifulSoup
from django.conf import settings
from django.urls import reverse, resolve, get_resolver
import requests
from urllib.parse import urljoin


class Command(BaseCommand):
    help = 'Build a search index of the GPE Club website content'

    def add_arguments(self, parser):
        parser.add_argument(
            '--base-url',
            default='http://localhost:8000',
            help='Base URL of the site to crawl',
        )

    def handle(self, *args, **options):
        base_url = options['base_url']
        self.stdout.write(f"Building site index from {base_url}")

        # Create the site index
        site_index = self.build_site_index(base_url)

        # Save the index to a JSON file
        index_path = os.path.join(settings.BASE_DIR, 'static', 'site_index.json')
        with open(index_path, 'w') as f:
            json.dump(site_index, f, indent=2)

        self.stdout.write(self.style.SUCCESS(f"Site index built and saved to {index_path}"))

    def build_site_index(self, base_url):
        """
        Build a site index by crawling the website
        """
        index = {}
        visited = set()
        to_visit = self.get_all_url_patterns()

        self.stdout.write(f"Found {len(to_visit)} URL patterns to visit")

        # Add manual descriptions for key pages
        page_descriptions = {
            '/': 'GPE Club home page with general information about the club and its projects.',
            '/projects/search/': 'Search for projects created by the GPE Club.',
            '/vocab/list': 'List of vocabulary sets for practice.',
            '/projects/school/': 'Access PowerSchool grade viewer and school-related tools.',
            '/about/': 'Information about the GPE Club and its members.',
            '/projects/trigonomis/': 'Trigonomis game project page with download links.',
            '/vocab/ai/set1/': 'AI-powered vocabulary practice for Set 1.',
            '/projects/powerschool/': 'PowerSchool grade viewer integration.'
        }

        # Crawl the site
        for url_path in to_visit:
            if url_path in visited:
                continue

            visited.add(url_path)
            full_url = urljoin(base_url, url_path)

            try:
                # Skip dynamic URLs with placeholders
                if '<' in url_path or '>' in url_path:
                    continue

                self.stdout.write(f"Visiting {full_url}")

                # For simplicity, we'll use pre-defined descriptions for key pages
                if url_path in page_descriptions:
                    content = page_descriptions[url_path]
                    title = url_path.split('/')[-2].capitalize() if url_path.endswith('/') else url_path.split('/')[
                        -1].capitalize()
                    if not title:
                        title = "Home"

                    index[url_path] = {
                        'title': title,
                        'content': content,
                        'keywords': self.extract_keywords(url_path, content)
                    }
                else:
                    # You could implement actual crawling here to extract content
                    # For simplicity, we're using predefined descriptions
                    continue

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing {url_path}: {e}"))

        return index

    def get_all_url_patterns(self):
        """
        Extract all URL patterns from the Django project
        """
        url_patterns = []

        def extract_urls(patterns, namespace=None, prefix=''):
            for pattern in patterns:
                if isinstance(pattern, URLResolver):
                    extract_urls(pattern.url_patterns, pattern.namespace, prefix + pattern.pattern.regex.pattern)
                elif isinstance(pattern, URLPattern) and hasattr(pattern, 'name') and pattern.name:
                    try:
                        url = reverse(pattern.name)
                        url_patterns.append(url)
                    except:
                        # Some URL patterns might require kwargs
                        pass

        extract_urls(get_resolver().url_patterns)

        # Add manual entries for pages with dynamic URLs
        url_patterns.extend([
            '/vocab/ai/set1/',
            '/vocab/ai/set2/',
            '/vocab/mcq/set1/',
            '/vocab/mcq/set2/',
            '/vocab/sets/set1/',
            '/vocab/sets/set2/',
        ])

        return url_patterns

    def extract_keywords(self, url, content):
        """
        Extract keywords from the URL and content
        """
        keywords = []

        # Extract from URL
        path_parts = [p for p in url.split('/') if p]
        keywords.extend(path_parts)

        # Extract from content
        if content:
            # Simple keyword extraction - split by spaces and punctuation
            words = content.lower().split()
            # Filter out common words and keep unique ones
            content_keywords = set([w.strip('.,!?():;') for w in words if len(w) > 4])
            keywords.extend(list(content_keywords)[:10])  # Limit to 10 keywords

        return list(set(keywords))  # Remove duplicates