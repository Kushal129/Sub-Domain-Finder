import requests
import sys
import os

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

            # return url  # Return the URL for saving to a file
        else:
            print(f"{RED}[-] Non-200 status code for ----> {url}{RESET}")
    except requests.ConnectionError:
        print(f"{RED}[-] Connection Error for ----> {url}{RESET}")
    except requests.Timeout:
        print(f"{RED}[-] Timeout Error for ----> {url}{RESET}")
    except requests.RequestException:
        print(f"{RED}[-] Failed to request ----> {url}{RESET}")
    return None

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

def main():
    intro()
    try:
        target_url = input("Enter Target URL (e.g., example.com): ").strip()
        subdomains_file = input("Enter path to subdomains file (e.g., Subdomain.txt): ").strip()
        protocol = input("Choose protocol (http [Enter-1] or https [Enter-2]): ").strip()

        if not target_url:
            print(f"{RED}[-] No target URL provided.{RESET}")
            sys.exit(1)
                    
        if protocol == '1':
            protocol = "http"
        elif protocol == '2':
            protocol = "https"
        else:
            print(f"{YELLOW}[-] Invalid choice. Defaulting to https.{RESET}")
            protocol = "https"

        # Expand user directory
        subdomains_file = os.path.expanduser(subdomains_file)
        
        if not os.path.isfile(subdomains_file):
            print(f"{RED}[-] The file '{subdomains_file}' does not exist.{RESET}")
            sys.exit(1)

        print(f"Using subdomains file: '{subdomains_file}'")
        discovered_subdomains = []

        with open(subdomains_file, "r") as wordlist:
            subdomains = [f"{protocol}://{line.strip()}.{target_url}" for line in wordlist]

        for index, subdomain in enumerate(subdomains, start=1):
            print(f"[*] Checking {index}/{len(subdomains)}: {subdomain}")
            discovered = request(subdomain)
            if discovered:
                discovered_subdomains.append(discovered)
        
        if discovered_subdomains:
            output_file = f"discovered_subdomains_{target_url}.txt"
            with open(output_file, "w") as f:
                for subdomain in discovered_subdomains:
                    f.write(subdomain + "\n")
            print(f"{GREEN}[+] Discovered subdomains saved to {output_file}{RESET}")
        else:
            print(f"{RED}[-] No subdomains discovered.{RESET}")

    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Interrupted! Exiting gracefully.{RESET}")
    except Exception as e:
        print(f"{RED}[-] An unexpected error occurred: {e}{RESET}")
    finally:
        print(f"\n{GREEN}Goodbye!{RESET}")

if __name__ == "__main__":
    main()

