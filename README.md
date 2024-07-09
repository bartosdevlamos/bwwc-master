# Baabs Wide Web Crawler

A web crawler designed to collect unique domain names starting from a given URL and save them to an Excel file.

## Structure

- `main.py`: The main script that runs the project.
- `print_art.py`: Contains ASCII art and disclaimer printing functions.
- `user_agents.py`: Contains user agent generation function.
- `utils.py`: Contains utility functions for crawling, domain extraction, and writing to Excel.

## How to Run

```bash
python main.py --starturl <start_url> --depth <max_depth> --threads <num_threads> --subdomains <true_or_false> --output <output_path>
