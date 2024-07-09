import argparse
from print_art import print_bwwc_art, print_disclaimer
from utils import crawl

def main():
    parser = argparse.ArgumentParser(description='Baabs wide Web domain crawler.')
    parser.add_argument('--starturl', required=True, help='The starting URL for the crawl')
    parser.add_argument('--depth', type=int, required=True, help='The depth of the crawl')
    parser.add_argument('--threads', type=int, default=10, help='The number of threads to use for crawling')
    parser.add_argument('--subdomains', type=bool, default=False, help='Whether to include subdomains (true or false)')
    parser.add_argument('--output', type=str, default='crawl_results.xlsx', help='The output path for the Excel file')
    
    args = parser.parse_args()

    start_url = args.starturl
    max_depth = args.depth
    num_threads = args.threads
    include_subdomains = args.subdomains
    output_path = args.output

    print_bwwc_art()
    print_disclaimer()

    try:
        crawl(start_url, max_depth, num_threads, include_subdomains, output_path)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Saving results...")
        sys.exit(0)

if __name__ == "__main__":
    main()
