import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from openpyxl import Workbook
from concurrent.futures import ThreadPoolExecutor, as_completed
import signal
import sys
from user_agents import generate_random_user_agent

def get_domains(url, include_subdomains):
    """Retrieve all unique domains from the given URL."""
    try:
        headers = {
            'X-Forwarded-For': '127.0.0.1',
            'X-Forwarded-Host': 'localhost',
            'User-Agent': generate_random_user_agent(),
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        domains = set()
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            full_url = urljoin(url, href)
            domain = urlparse(full_url).netloc
            if domain:
                if not include_subdomains:
                    domain = get_base_domain(domain)
                domains.add(domain)
        return domains
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return set()

def get_base_domain(domain):
    """Get the base domain, excluding subdomains."""
    parts = domain.split('.')
    if len(parts) > 2:
        return '.'.join(parts[-2:])
    return domain

def write_to_excel(data, output_path):
    """Write the collected data to an Excel file."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Crawl Results"
    
    # Write the header
    ws.append(["Crawl Depth", "Domain"])

    # Write the data
    for depth, domains in data.items():
        for domain in domains:
            ws.append([depth, domain])

    # Save the workbook
    wb.save(output_path)
    print(f"Results saved to {output_path}")

def crawl_page(url, include_subdomains):
    """Helper function to be used with threading."""
    return url, get_domains(url, include_subdomains)

def crawl(start_url, max_depth, num_threads, include_subdomains, output_path):
    """Crawl the web starting from start_url up to max_depth."""
    to_crawl = {0: [start_url]}
    seen = set()
    results = {}

    def signal_handler(sig, frame):
        nonlocal results
        write_to_excel(results, output_path)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    for depth in range(max_depth + 1):
        current_depth_urls = to_crawl.get(depth, [])
        if not current_depth_urls:
            break
        
        next_depth_urls = []
        results[depth] = set()

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_url = {executor.submit(crawl_page, url, include_subdomains): url for url in current_depth_urls}
            for future in as_completed(future_to_url):
                url, domains = future.result()
                if url in seen:
                    continue
                seen.add(url)
                results[depth].update(domains)

                for domain in domains:
                    if domain not in seen:
                        next_depth_urls.append(f"https://{domain}")

        if next_depth_urls:
            to_crawl[depth + 1] = next_depth_urls

    write_to_excel(results, output_path)
