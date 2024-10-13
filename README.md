# Recon Automation Script

This repository contains a Python script that automates various reconnaissance tasks on Kali Linux. It integrates with built-in Kali tools and performs DNS enumeration, subdomain enumeration, and basic vulnerability checks.

## Features

- **DNS Enumeration**: Retrieves DNS records such as A, AAAA, MX, NS, SOA, and TXT.
- **Subdomain Enumeration**: Discovers subdomains using a customizable wordlist.
- **Integration with theHarvester**: Gathers additional hosts and emails from public sources.
- **Basic Vulnerability Checks**: Identifies directory listings and default web pages.

## Requirements

- **Operating System**: Kali Linux (or any Linux distribution with necessary tools installed)
- **Python 3**: Ensure Python 3 is installed.
- **Python Packages**: Install packages from `requirements.txt`.
- **Kali Tools**: Ensure `theHarvester` is installed (it comes pre-installed on Kali Linux).

## Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/akjalbani/recon-tools-py.git
    
    ```

2. **Install Python Dependencies**:

    ```bash
    sudo pip3 install -r requirements.txt
    ```

3. **Make the Script Executable**:

    ```bash
    chmod +x recon_automation.py
    ```

## Usage

```bash
./recon_automation.py -d example.com -w subdomains.txt


