# SubDomain Finder Tool

## Overview

The **SubDomain Finder Tool** is a Python script designed to discover subdomains of a target domain. It uses a wordlist to generate potential subdomains and checks their availability via HTTP or HTTPS requests. This tool helps identify potential subdomains that may not be immediately visible or listed.

## Features

- **Custom User-Agent**: Avoid basic request blocks by using a custom User-Agent header.
- **Protocol Selection**: Choose between HTTP and HTTPS protocols for requests.
- **Progress Indicator**: View progress updates while subdomains are being checked.
- **Error Handling**: Graceful handling of connection errors, timeouts, and non-200 status codes.
<!-- - **Intro Screen**: Displays a custom ASCII art logo and introductory text. -->
<!-- - **Result Saving**: Saves discovered subdomains to a text file for easy access. -->

## Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Kushal129/SubDomain-Finder-Tool.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd SubDomain-Finder-Tool
   ```

3. **Install the required dependencies:**
   ```bash
   pip install requests
   ```

4. **Run the script:**
   ```bash
    python SubDomain.py
   ```

## Usage

1. **Enter the target URL** (e.g., `example.com`).
2. **Provide the path to the subdomains file** (e.g., `Subdomain.txt`). You can download a subdomains list file from [this link](https://github.com/Kushal129/Sub-Domain-Finder/blob/main/Subdomain.txt).
3. **Choose the protocol** (HTTP or HTTPS).


## Contributing

Contributions are welcome! If you have suggestions or improvements, please create a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please reach out to [Kushal129](https://github.com/Kushal129/).


