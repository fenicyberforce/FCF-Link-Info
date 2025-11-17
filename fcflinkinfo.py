#!/usr/bin/env python3
"""
FCF LINK INFO - Advanced Information Extraction Tool
Developer: Feni Cyber Force
Version: 3.1.1
"""

import os
import sys
import time
import json
import platform
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path
import socket
import uuid
import getpass
import threading
import random
import re

# Third-party imports
try:
    import httpx
    import requests
    from colorama import Fore, Style, init
    from tqdm import tqdm
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Please run: pip install httpx requests colorama tqdm")
    sys.exit(1)

# Initialize colorama
init(autoreset=True)

# Tool Information
TOOL_NAME = "FCF LINK INFO"
VERSION = "3.1.1"
DEVELOPER = "Feni Cyber Force"
FACEBOOK_PAGE = "https://www.facebook.com/feni_cyber_force_official"
TELEGRAM_CHANNEL = "https://t.me/feni_cyber_force"
TELEGRAM_HELPLINE = "@FCF_helping_bot"

class Colors:
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    BRIGHT = Style.BRIGHT
    RESET = Style.RESET_ALL

class FCFPrinter:
    def __init__(self):
        self.max_len = 0
    
    def print_animated(self, text, delay=0.03):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def loading_animation(self, text, duration=2):
        symbols = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        start_time = time.time()
        i = 0
        
        while time.time() - start_time < duration:
            print(f"\r{Colors.CYAN}{symbols[i % len(symbols)]} {text}{Colors.RESET}", end='')
            i += 1
            time.sleep(0.1)
        print(f"\r{Colors.GREEN}✅ {text} Complete!{Colors.RESET}")

class FCFBanner:
    @staticmethod
    def show():
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Big "F C F" ASCII Banner Design - Three separate letters with spaces
        print(f"{Colors.CYAN}{Colors.BRIGHT}")
        print("███████╗      ██████╗     ███████╗")
        print("██╔════╝     ██╔════╝     ██╔════╝")
        print("█████╗       ██║          █████╗  ")
        print("██╔══╝       ██║          ██╔══╝  ")
        print("██║          ╚██████╗     ██║")
        print("╚═╝           ╚═════╝     ╚═╝")
        print(f"{Colors.RESET}")
        
        # Info Box - Fixed Facebook URL
        print(f"{Colors.GREEN}{Colors.BRIGHT}")
        print("┌────────────────────────────────────────────────────────┐")
        print("│              FENI CYBER FORCE                          │")
        print("│              ADVANCED DOCUMENT ANALYZER                │")
        print("│              Version 3.1.1                             │")
        print("│                                                        │")
        print("│    Facebook: facebook.com/feni_cyber_force_official    │")
        print("│    Telegram: t.me/feni_cyber_force                     │")
        print("│    Helpline: @FCF_helping_bot                          │")
        print("│    Developer: Feni Cyber Force                         │")
        print("│                                                        │")
        print("└────────────────────────────────────────────────────────┘")
        print(f"{Colors.RESET}")
        print()

class PasswordGenerator:
    @staticmethod
    def generate_password_ideas(owner_name=None, email=None, document_info=None):
        """Generate intelligent password guesses based on available information"""
        ideas = []
        
        # Extract name parts from owner name
        name_parts = []
        if owner_name:
            name_parts = re.findall(r'\b\w+\b', owner_name.lower())
        
        # Extract username from email
        email_user = None
        if email and '@' in email:
            email_user = email.split('@')[0].lower()
        
        # Common password patterns
        common_suffixes = ['123', '1234', '12345', '123456', '!', '@', '#', '1', '2', '2020', '2021', '2022', '2023', '2024']
        
        # Generate ideas based on available info
        if name_parts:
            first_name = name_parts[0]
            last_name = name_parts[-1] if len(name_parts) > 1 else ""
            
            # Combination with common suffixes
            for suffix in common_suffixes[:3]:
                ideas.append(f"{first_name}{suffix}")
                if last_name:
                    ideas.append(f"{first_name}{last_name}{suffix}")
                    ideas.append(f"{first_name[0]}{last_name}{suffix}")
            
            # Capitalization variations
            ideas.append(f"{first_name.capitalize()}{common_suffixes[0]}")
            if last_name:
                ideas.append(f"{first_name.capitalize()}{last_name.capitalize()}")
        
        if email_user:
            # Email username based passwords
            for suffix in common_suffixes[:2]:
                ideas.append(f"{email_user}{suffix}")
            
            # Add some variations
            ideas.append(f"{email_user}!")
            ideas.append(f"{email_user}@123")
        
        # Add some common passwords if we don't have enough ideas
        common_passwords = [
            "password123", "admin123", "welcome123", 
            "qwerty123", "letmein123", "monkey123"
        ]
        
        while len(ideas) < 5:
            new_pass = random.choice(common_passwords)
            if new_pass not in ideas:
                ideas.append(new_pass)
        
        # Ensure we have exactly 5 unique ideas
        return list(set(ideas))[:5]

class GoogleDocExtractor:
    def __init__(self):
        self.printer = FCFPrinter()
    
    def extract_info(self, doc_link):
        self.printer.loading_animation("Analyzing Google Document", 3)
        
        # Extract document ID from URL
        doc_id = None
        patterns = [
            r'/d/([a-zA-Z0-9_-]+)',
            r'/folders/([a-zA-Z0-9_-]+)',
            r'id=([a-zA-Z0-9_-]+)',
            r'[a-zA-Z0-9_-]{25,}'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, doc_link)
            if match:
                doc_id = match.group(1) if len(match.groups()) > 0 else match.group(0)
                break
        
        if not doc_id:
            return {"Error": "❌ Document ID not found in the provided URL"}
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "X-Origin": "https://drive.google.com"
        }
        
        try:
            url = f"https://www.googleapis.com/drive/v3/files/{doc_id}?fields=*&key=AIzaSyC1eQ1xj69IdTMeii5r7brs3R90eck-m7k"
            response = httpx.get(url, headers=headers, timeout=10)
            
            if response.status_code == 404:
                return {"Error": "❌ File not found or not publicly accessible"}
            elif response.status_code == 403:
                return {"Error": "❌ Access denied. The document may not be publicly accessible"}
            elif response.status_code != 200:
                return {"Error": f"❌ API request failed with status {response.status_code}"}
            
            data = response.json()
            return self._parse_document_data(data)
            
        except httpx.RequestError as e:
            return {"Error": f"❌ Network error: {str(e)}"}
        except json.JSONDecodeError:
            return {"Error": "❌ Invalid response from Google API"}
        except Exception as e:
            return {"Error": f"❌ Unexpected error: {str(e)}"}
    
    def _parse_document_data(self, data):
        result = {}
        
        # Basic Document Info
        try:
            result['📄 Document ID'] = data.get('id', 'Unknown')
            result['📝 Title'] = data.get('name', 'Unknown')
            result['📋 Description'] = data.get('description', 'Not available')
            result['💾 File Size'] = self._format_file_size(data.get('size', 0))
            result['🖼️ Icon Link'] = data.get('iconLink', 'Not available')
            result['🔗 Web View Link'] = data.get('webViewLink', 'Not available')
        except:
            pass
        
        # Dates
        try:
            created_date = data.get('createdTime', '')
            modified_date = data.get('modifiedTime', '')
            
            if created_date:
                created_date = datetime.fromisoformat(created_date.replace('Z', '+00:00'))
                result['📅 Created Date'] = created_date.strftime('%Y/%m/%d %H:%M:%S UTC')
            
            if modified_date:
                modified_date = datetime.fromisoformat(modified_date.replace('Z', '+00:00'))
                result['🕒 Last Modified'] = modified_date.strftime('%Y/%m/%d %H:%M:%S UTC')
                
        except:
            pass
        
        # Owner Information
        try:
            owners = data.get('owners', [])
            if owners:
                owner = owners[0]
                owner_info = {
                    '👤 Name': owner.get('displayName', 'Unknown'),
                    '📧 Email': owner.get('emailAddress', 'Unknown'),
                    '🆔 Google ID': owner.get('id', 'Unknown'),
                    '📊 Type': 'user',
                    '🖼️ Photo': owner.get('photoLink', 'Not available')
                }
                result['👑 Document Owner'] = owner_info
        except:
            pass
        
        # Permissions
        try:
            permissions = data.get('permissions', [])
            public_perms = []
            for perm in permissions:
                if perm.get('type') in ['anyone', 'domain']:
                    public_perms.append({
                        '🔐 Role': perm.get('role', 'Unknown'),
                        '📋 Type': perm.get('type', 'Unknown'),
                        '➕ Additional Roles': perm.get('additionalRoles', [])
                    })
            
            if public_perms:
                result['🌐 Public Permissions'] = public_perms
        except:
            pass
            
        # Capabilities
        try:
            capabilities = data.get('capabilities', {})
            result['⚙️ Document Capabilities'] = {
                '✏️ Can Edit': capabilities.get('canEdit', False),
                '📥 Can Download': capabilities.get('canDownload', False),
                '💬 Can Comment': capabilities.get('canComment', False),
                '🏷️ Can Rename': capabilities.get('canRename', False)
            }
        except:
            pass
            
        # MIME Type
        try:
            mime_type = data.get('mimeType', 'Unknown')
            result['📄 MIME Type'] = mime_type
            if 'folder' in mime_type:
                result['📁 Type'] = 'Google Folder'
            elif 'document' in mime_type:
                result['📄 Type'] = 'Google Document'
            elif 'spreadsheet' in mime_type:
                result['📊 Type'] = 'Google Spreadsheet'
            elif 'presentation' in mime_type:
                result['🎤 Type'] = 'Google Presentation'
        except:
            pass
            
        return result
    
    def _format_file_size(self, size_bytes):
        if not size_bytes or size_bytes == 0:
            return "Unknown"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

class FCFLinkInfo:
    def __init__(self):
        self.printer = FCFPrinter()
        self.banner = FCFBanner()
        self.running = True
        self.social_opened = False
        
    def open_social_links_correct_sequence(self):
        """Open social media links in EXACT correct sequence"""
        if self.social_opened:
            return
            
        print(f"\n{Colors.YELLOW}{Colors.BRIGHT}🔗 OPENING OFFICIAL CHANNELS...{Colors.RESET}")
        print()
        
        # STEP 1: Open Facebook instantly when tool starts
        print(f"{Colors.BLUE}📘 Opening Facebook Page...{Colors.RESET}")
        try:
            if platform.system() == "Linux" and "ANDROID_ROOT" in os.environ:  # Termux
                subprocess.run(["termux-open-url", FACEBOOK_PAGE], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                webbrowser.open(FACEBOOK_PAGE, new=2)
            print(f"{Colors.GREEN}✅ Facebook opened successfully!{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}❌ Failed to open Facebook: {e}{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}Please visit our Facebook page and return to this terminal.{Colors.RESET}")
        print(f"{Colors.YELLOW}After visiting Facebook, press Enter to continue...{Colors.RESET}")
        input(f"\n{Colors.GREEN}Press Enter after visiting Facebook...{Colors.RESET}")
        
        # STEP 2: Open Telegram ONLY after user returns and presses Enter
        print(f"\n{Colors.GREEN}📢 Opening Telegram Channel...{Colors.RESET}")
        try:
            if platform.system() == "Linux" and "ANDROID_ROOT" in os.environ:  # Termux
                subprocess.run(["termux-open-url", TELEGRAM_CHANNEL], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                webbrowser.open(TELEGRAM_CHANNEL, new=2)
            print(f"{Colors.GREEN}✅ Telegram opened successfully!{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}❌ Failed to open Telegram: {e}{Colors.RESET}")
        
        # Beautiful completion message - Fixed the text
        print(f"\n{Colors.GREEN}{Colors.BRIGHT}┌────────────────────────────────────────────────────────┐")
        print("│              CHANNELS OPENED SUCCESSFULLY              │")
        print("└────────────────────────────────────────────────────────┘")
        print(f"\n{Colors.CYAN}📱 Thank you for supporting Feni Cyber Force!{Colors.RESET}")
        print(f"{Colors.YELLOW}🌟 Please follow both channels for updates and support{Colors.RESET}")
        print(f"{Colors.MAGENTA}🚀 Ready to analyze documents...{Colors.RESET}")
        
        input(f"\n{Colors.GREEN}Press Enter to continue to main menu...{Colors.RESET}")
        self.social_opened = True

    def display_results(self, results):
        """Display analysis results in a beautiful formatted way"""
        if 'Error' in results:
            print(f"\n{Colors.RED}{Colors.BRIGHT}┌────────────────────────────────────────────────────────┐")
            print("│                    ANALYSIS FAILED                     │")
            print("└────────────────────────────────────────────────────────┘")
            print(f"\n   {Colors.RED}❌ {results['Error']}{Colors.RESET}")
            return
        
        print(f"\n{Colors.GREEN}{Colors.BRIGHT}┌────────────────────────────────────────────────────────┐")
        print("│              DOCUMENT ANALYSIS RESULTS              │")
        print("└────────────────────────────────────────────────────────┘{Colors.RESET}")
        
        # Display basic document information
        basic_info_shown = False
        for key, value in results.items():
            if key not in ['👑 Document Owner', '🌐 Public Permissions', '⚙️ Document Capabilities']:
                if not basic_info_shown:
                    print(f"\n{Colors.CYAN}{Colors.BRIGHT}📄 BASIC DOCUMENT INFO:{Colors.RESET}")
                    basic_info_shown = True
                print(f"   {Colors.YELLOW}{key}:{Colors.RESET} {Colors.WHITE}{value}{Colors.RESET}")
        
        # Display owner information
        if '👑 Document Owner' in results:
            print(f"\n{Colors.GREEN}{Colors.BRIGHT}👑 DOCUMENT OWNER INFORMATION:{Colors.RESET}")
            owner = results['👑 Document Owner']
            for key, value in owner.items():
                print(f"   {Colors.CYAN}{key}:{Colors.RESET} {Colors.WHITE}{value}{Colors.RESET}")
            
            # Generate password ideas based on owner info
            print(f"\n{Colors.MAGENTA}{Colors.BRIGHT}🔐 PASSWORD SECURITY ANALYSIS:{Colors.RESET}")
            print(f"   {Colors.YELLOW}Based on owner information, possible password patterns:{Colors.RESET}")
            print()
            
            password_ideas = PasswordGenerator.generate_password_ideas(
                owner_name=owner.get('👤 Name'),
                email=owner.get('📧 Email'),
                document_info=results
            )
            
            for i, password in enumerate(password_ideas, 1):
                print(f"   {Colors.RED}{i}. {password}{Colors.RESET}")
            
            print(f"\n   {Colors.YELLOW}💡 Note: These are common patterns for educational purposes only{Colors.RESET}")
        
        # Display permissions
        if '🌐 Public Permissions' in results:
            print(f"\n{Colors.BLUE}{Colors.BRIGHT}🌐 PUBLIC PERMISSIONS:{Colors.RESET}")
            for perm in results['🌐 Public Permissions']:
                for key, value in perm.items():
                    print(f"   {Colors.CYAN}{key}:{Colors.RESET} {Colors.WHITE}{value}{Colors.RESET}")
        
        # Display capabilities
        if '⚙️ Document Capabilities' in results:
            print(f"\n{Colors.GREEN}{Colors.BRIGHT}⚙️ DOCUMENT CAPABILITIES:{Colors.RESET}")
            caps = results['⚙️ Document Capabilities']
            for cap, value in caps.items():
                status = f"{Colors.GREEN}✅ Yes{Colors.RESET}" if value else f"{Colors.RED}❌ No{Colors.RESET}"
                print(f"   {Colors.CYAN}{cap}:{Colors.RESET} {status}")

    def google_document_analyzer(self):
        self.banner.show()
        print(f"{Colors.CYAN}{Colors.BRIGHT}┌────────────────────────────────────────────────────────┐")
        print("│              GOOGLE DOCUMENT ANALYZER               │")
        print("└────────────────────────────────────────────────────────┘{Colors.RESET}")
        print(f"{Colors.YELLOW}Advanced metadata extraction and security analysis{Colors.RESET}\n")
        
        doc_url = input(f"{Colors.YELLOW}📎 Enter Google Document URL: {Colors.RESET}").strip()
        
        if not doc_url:
            print(f"{Colors.RED}❌ No URL provided!{Colors.RESET}")
            time.sleep(2)
            return
        
        if 'docs.google.com' not in doc_url and 'drive.google.com' not in doc_url:
            print(f"{Colors.RED}❌ Please provide a valid Google Docs or Drive URL{Colors.RESET}")
            time.sleep(2)
            return
        
        extractor = GoogleDocExtractor()
        results = extractor.extract_info(doc_url)
        
        self.display_results(results)
        
        # Beautiful continue prompt
        print(f"\n{Colors.GREEN}{Colors.BRIGHT}┌────────────────────────────────────────────────────────┐")
        print("│                 ANALYSIS COMPLETE                      │")
        print("└────────────────────────────────────────────────────────┘")
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    def show_menu(self):
        menu = f"""
{Colors.CYAN}{Colors.BRIGHT}┌────────────────────────────────────────────────────────┐
│                    FCF MAIN MENU                       │
└────────────────────────────────────────────────────────┘{Colors.RESET}

{Colors.GREEN}1.{Colors.RESET} 📄 Google Document Analyzer
{Colors.RED}0.{Colors.RESET} 🚪 Exit

{Colors.YELLOW}Choose an option [0-1]: {Colors.RESET}"""
        return input(menu)

    def run(self):
        # Show banner first with important info
        self.banner.show()
        
        # Then open social links in EXACT correct sequence
        self.open_social_links_correct_sequence()
        
        while self.running:
            self.banner.show()
            choice = self.show_menu()
            
            if choice == '1':
                self.google_document_analyzer()
            elif choice == '0':
                self.exit_tool()
            else:
                print(f"\n{Colors.RED}❌ Invalid option! Please try again.{Colors.RESET}")
                time.sleep(1)

    def exit_tool(self):
        self.banner.show()
        print(f"\n{Colors.GREEN}{Colors.BRIGHT}┌────────────────────────────────────────────────────────┐")
        print("│              THANK YOU FOR USING FCF               │")
        print("└────────────────────────────────────────────────────────┘{Colors.RESET}")
        print(f"\n{Colors.YELLOW}📱 Don't forget to follow our official channels:{Colors.RESET}")
        print(f"{Colors.BLUE}📘 Facebook: {FACEBOOK_PAGE}{Colors.RESET}")
        print(f"{Colors.GREEN}📢 Telegram: {TELEGRAM_CHANNEL}{Colors.RESET}")
        print(f"\n{Colors.MAGENTA}{Colors.BRIGHT}👋 See you next time!{Colors.RESET}\n")
        self.running = False

def main():
    try:
        tool = FCFLinkInfo()
        tool.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}❌ Tool interrupted by user. Goodbye!{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}💥 An error occurred: {str(e)}{Colors.RESET}")

if __name__ == "__main__":
    main()