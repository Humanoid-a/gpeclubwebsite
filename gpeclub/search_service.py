# gpeclub/search_service.py
import json
import os
import re
from django.conf import settings
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

# Download NLTK resources if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class ContentSearchService:
    def __init__(self):
        self.index_path = os.path.join(settings.BASE_DIR, 'static', 'site_index.json')
        self.site_index = self.load_index()
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))

    def load_index(self):
        """Load the site index from the JSON file"""
        if os.path.exists(self.index_path):
            with open(self.index_path, 'r') as f:
                return json.load(f)
        return {}

    def preprocess_text(self, text):
        """Preprocess text for searching: tokenize, remove stop words, stem"""
        if not text:
            return []

        # Tokenize and convert to lowercase
        tokens = word_tokenize(text.lower())

        # Remove stop words and punctuation
        tokens = [t for t in tokens if t.isalnum() and t not in self.stop_words]

        # Stem words
        stemmed_tokens = [self.stemmer.stem(t) for t in tokens]

        return stemmed_tokens

    def search(self, query, max_results=5):
        """Search the site index for content matching the query"""
        query_tokens = self.preprocess_text(query)

        if not query_tokens or not self.site_index:
            return []

        # Calculate relevance scores for each page
        scores = {}
        for url, page_info in self.site_index.items():
            score = self.calculate_relevance(query_tokens, page_info)
            if score > 0:
                scores[url] = score

        # Sort by score
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # Format results
        results = []
        for url, score in sorted_results[:max_results]:
            results.append({
                'url': url,
                'title': self.site_index[url]['title'],
                'content': self.site_index[url]['content'],
                'score': score
            })

        return results

    def calculate_relevance(self, query_tokens, page_info):
        """Calculate relevance score for a page based on query tokens"""
        if not query_tokens:
            return 0

        # Preprocess page content
        content_tokens = self.preprocess_text(page_info['content'])
        title_tokens = self.preprocess_text(page_info['title'])
        keyword_tokens = []
        for keyword in page_info.get('keywords', []):
            keyword_tokens.extend(self.preprocess_text(keyword))

        # Count matches in different parts with different weights
        title_matches = sum(1 for token in query_tokens if token in title_tokens)
        content_matches = sum(1 for token in query_tokens if token in content_tokens)
        keyword_matches = sum(1 for token in query_tokens if token in keyword_tokens)

        # Calculate weighted score
        score = (title_matches * 3) + (content_matches * 1) + (keyword_matches * 2)

        return score

    def get_context_for_query(self, query, max_results=3):
        """Get context about the site for the given query"""
        results = self.search(query, max_results)

        if not results:
            return "No specific information found about your query."

        context = "Here's what I found on the GPE Club website:\n\n"
        for result in results:
            context += f"Page: {result['title']}\n"
            context += f"Content: {result['content']}\n"
            context += f"URL: {result['url']}\n\n"

        return context