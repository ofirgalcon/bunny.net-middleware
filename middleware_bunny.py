#!/usr/local/munki/munki-python

# munki URL processor for bunny.net CDN with token security 
# https://docs.bunny.net/docs/cdn-token-authentication-basic

# requires bunny.net CDN pull zone key 
# defaults write /private/var/root/Library/Preferences/ManagedInstallsProc bunny_key "YOUR_BUNNY_KEY"

from urllib.parse import quote, urlparse, urlencode, unquote
import hashlib
from base64 import b64encode
import time
import subprocess

__version__ = '1.0.5'

def get_token_security_key():
    """Retrieve the TOKEN_SECURITY_KEY using the defaults read command."""
    try:
        result = subprocess.run(
            ["defaults", "read", "/private/var/root/Library/Preferences/ManagedInstallsProc", "bunny_key"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error reading TOKEN_SECURITY_KEY: {e}")
        return None

def generate_token(security_key, original_path, expires, filtered_ip=""):
    """Generate BunnyCDN URL authentication token based on the security key, original URL path, and expiration time."""
    token_content = f'{security_key}{original_path}{expires}{filtered_ip}'
    md5sum = hashlib.md5()
    md5sum.update(token_content.encode('ascii'))
    token_digest = md5sum.digest()
    token_base64 = b64encode(token_digest).decode('ascii')
    
    # Perform URL-safe Base64 encoding
    token_formatted = token_base64.replace('\n', '').replace('+', '-').replace('/', '_').replace('=', '')
    
    return token_formatted

def encode_params(data):
    """Encode parameters for the URL."""
    return urlencode(data, doseq=True)

def process_request_options(options):
    """Process request options to include token and expiration if the URL contains 'cdn.net'."""
    url = options.get("url")
    if "cdn.net" in url:
        # Get the token security key
        TOKEN_SECURITY_KEY = get_token_security_key()
        if not TOKEN_SECURITY_KEY:
            print("Failed to retrieve TOKEN_SECURITY_KEY. Exiting.")
            return options
        
        # Parse the URL to extract the path
        parsed_url = urlparse(url)
        url_path = parsed_url.path

        # Unquote the path to ensure it hasn't been double encoded
        original_path = unquote(url_path)

        # Calculate the expiration timestamp (e.g., 1 hour from now)
        expires = int(time.time()) + 3600
        
        # Generate the token using the security key, the unencoded URL path, and expiration time
        token = generate_token(TOKEN_SECURITY_KEY, original_path, expires)
        
        # Add token and expiration to query parameters
        query_params = {
            "token": token,
            "expires": expires
        }

        # Concat the URL and query string using the encoded path
        encoded_url_path = quote(original_path)
        options["url"] = f'{parsed_url.scheme}://{parsed_url.netloc}{encoded_url_path}?{encode_params(query_params)}'
    
    return options

# # Example usage
# options_1 = {"url": "https://test.b-cdn.net/someinstaller.dmg"}
# processed_options_1 = process_request_options(options_1)
# print(f"Processed URL 1: {processed_options_1['url']}")

# options_2 = {"url": "https://example.com/assets/asasas.ico"}
# processed_options_2 = process_request_options(options_2)
# print(f"Processed URL 2: {processed_options_2['url']}")
