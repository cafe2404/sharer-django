

from bs4 import BeautifulSoup
from .models import Platform
from urllib.parse import urljoin
from django.urls import reverse

class CustomPlatform:
    
    @staticmethod
    def parser_html(platform:Platform,content):
        soup = BeautifulSoup(content, 'html.parser')
        # Kiểm tra nếu thẻ <head> không có, tạo mới thẻ <head>
        if platform.css_text and soup.head:
            style_tag = soup.new_tag('style')
            style_tag.string = platform.css_text
            soup.head.append(style_tag)
        # Update URLs in tags
        for tag in soup.find_all(['form', 'img', 'script', 'link', 'source']):
            if tag.get('href') and not tag['href'].startswith('http'):
                tag['href'] = urljoin(platform.url, tag['href'])
            if tag.get('action') and not tag['action'].startswith('http'):
                tag['action'] = urljoin(platform.url, tag['action'])
            if tag.get('src') and not tag['src'].startswith('http'):
                tag['src'] = urljoin(platform.url, tag['src'])
            if tag.get('srcset') and not tag['srcset'].startswith('http'):
                tag['srcset'] = urljoin(platform.url, tag['srcset'])
        return str(soup)
