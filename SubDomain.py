import requests
import sys
import os
import signal
import logging

# Define color codes
WHITE = "\033[0;37m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
RESET = "\033[0m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
BYELLOW = "\033[1;33m"
YELLOW = "\033[0;33m"

HYPERLINK = "\033]8;;{url}\033\\{text}\033]8;;\033\\"


DEFAULT_SUBDOMAINS_URL = "https://github.com/Kushal129/Sub-Domain-Finder/raw/main/Subdomain.txt"

# Setup logging
logging.basicConfig(filename="subdomain_finder.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Signal handler for graceful exit
def signal_handler(sig, frame):
    print(f"\n{YELLOW}[!] Interrupted! Exiting gracefully.{RESET}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def request(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        result = requests.get(url, headers=headers, timeout=5)
        if result.status_code == 200:
            output = (
                f"{GREEN}[+] Subdomain discovered!\n"
                f"{'-' * 50}\n"
                f"{BLUE}🔗 URL: {HYPERLINK.format(url=url, text=url)}\n"
                f"{GREEN}{'-' * 50}{RESET}\n"
            )
            print(output)
            logging.info(f"Subdomain discovered: {url}")
        else:
            print(f"{RED}[-] Non-200 status code for ----> {url}{RESET}")
            logging.info(f"Non-200 status code for {url}")
    except requests.ConnectionError:
        print(f"{RED}[-] Connection Error for ----> {url}{RESET}")
        logging.error(f"Connection Error for {url}")
    except requests.Timeout:
        print(f"{RED}[-] Timeout Error for ----> {url}{RESET}")
        logging.error(f"Timeout Error for {url}")
    except requests.RequestException:
        print(f"{RED}[-] Failed to request ----> {url}{RESET}")
        logging.error(f"Failed to request {url}")

def intro():
    border = "*" * 55
    title = "SubDomain Finder Tool"
    subtitle = "GitHub: www.github.com/Kushal129/"
    
    # ASCII Art for KHP Logo (Text Representation)
    khp_logo = """
    
         /$$   /$$ /$$   /$$ /$$$$$$$ 
        | $$  /$$/| $$  | $$| $$__  $$
        | $$ /$$/ | $$  | $$| $$  \ $$
        | $$$$$/  | $$$$$$$$| $$$$$$$/
        | $$  $$  | $$__  $$| $$____/ 
        | $$\  $$ | $$  | $$| $$      
        | $$ \  $$| $$  | $$| $$      
        |__/  \__/|__/  |__/|__/  
           
    """

    # Centering the title and subtitle
    khp_logo = f"{' ' * ((50 - len(khp_logo)) // 2)}{khp_logo}"
    title_line = f"{' ' * ((50 - len(title)) // 2)}{title}"
    subtitle_line = f"{' ' * ((50 - len(subtitle)) // 2)}{subtitle}"

    # Printing the intro
    print(f"\n{GREEN}{border}{RESET}")
    print(f"{PURPLE}{khp_logo}{RESET}")
    print(f"{BYELLOW}{title_line}{RESET}")
    print(f"{BYELLOW}{subtitle_line}{RESET}")
    print(f"{GREEN}{border}{RESET}\n")
    
def download_default_subdomains_file(file_path):
    try:
        response = requests.get(DEFAULT_SUBDOMAINS_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors
        with open(file_path, "w") as file:
            file.write(response.text)
        print(f"{GREEN}[+] Default subdomains file downloaded and saved to {file_path}{RESET}")
    except requests.RequestException as e:
        print(f"{RED}[-] Failed to download default subdomains file: {e}{RESET}")
        sys.exit(1)

def main():
    intro()
    try:
        target_url = input("Enter Target URL (e.g., example.com): ").strip()
        if not target_url:
            print(f"{RED}[-] No target URL provided.{RESET}")
            sys.exit(1)

        # Set default subdomains file path
        subdomains_file = "default_subdomains.txt"

        # Check if the default subdomains file already exists
        if os.path.isfile(subdomains_file):
            print(f"{GREEN}Using existing subdomains file: '{subdomains_file}'{RESET}")
        else:
            print(f"{YELLOW}Default subdomains file not found.{RESET}")
            # Option to choose between custom subdomains file or default file
            choice = input("Choose an option:\n1. Provide your own subdomains file\n2. Download default subdomains file\nEnter choice (1 or 2): ").strip()

            if choice == '1':
                subdomains_file = input("Enter path to subdomains file (e.g., Subdomain.txt): ").strip()
            elif choice == '2':
                download_default_subdomains_file(subdomains_file)
            else:
                print(f"{YELLOW}[-] Invalid choice. Defaulting to using the default subdomains file.{RESET}")
                download_default_subdomains_file(subdomains_file)

        # Expand user directory
        subdomains_file = os.path.expanduser(subdomains_file)
        
        if not os.path.isfile(subdomains_file):
            print(f"{RED}[-] The file '{subdomains_file}' does not exist.{RESET}")
            sys.exit(1)

        print(f"Using subdomains file: '{subdomains_file}'")
        discovered_subdomains = []

        protocol = input("Choose protocol (http [Enter-1] or https [Enter-2]): ").strip()
        if protocol == '1':
            protocol = "http"
        elif protocol == '2':
            protocol = "https"
        else:
            print(f"{YELLOW}[-] Invalid choice. Defaulting to https.{RESET}")
            protocol = "https"

        with open(subdomains_file, "r") as wordlist:
            subdomains = [f"{protocol}://{line.strip()}.{target_url}" for line in wordlist]

        for index, subdomain in enumerate(subdomains, start=1):
            print(f"[*] Checking {index}/{len(subdomains)}: {subdomain}")
            request(subdomain)
        
        if discovered_subdomains:
            output_file = f"discovered_subdomains_{target_url}.txt"
            with open(output_file, "w") as f:
                for subdomain in discovered_subdomains:
                    f.write(subdomain + "\n")
            print(f"{GREEN}[+] Discovered subdomains saved to {output_file}{RESET}")
            logging.info(f"Discovered subdomains saved to {output_file}")
        else:
            print(f"{RED}[-] No subdomains discovered.{RESET}")
            logging.info("No subdomains discovered.")

    except KeyboardInterrupt:
       
        print(f"\n{YELLOW}[!] Interrupted! Exiting gracefully.{RESET}")
    except Exception as e:
        print(f"{RED}[-] An unexpected error occurred: {e}{RESET}")
    finally:
        print(f"\n{GREEN}Goodbye!{RESET}")

if __name__ == "__main__":
    main()