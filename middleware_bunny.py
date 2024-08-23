#!/usr/local/munki/munki-python

# munki URL processor for bunny.net CDN with token security 
# https://docs.bunny.net/docs/cdn-token-authentication-basic

# requires bunny.net CDN pull zone key 
# defaults write /private/var/root/Library/Preferences/ManagedInstallsProc bunny_key "YOUR_BUNNY_KEY"

import hashlib
from base64 import b64encode
from urllib.parse import urlencode, urlparse, quote
import time
import subprocess

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

def generate_token(security_key, url_path, expires, filtered_ip=""):
    """Generate BunnyCDN URL authentication token based on the security key, URL path, and expiration time."""
    token_content = f'{security_key}{url_path}{expires}{filtered_ip}'
    md5sum = hashlib.md5()
    md5sum.update(token_content.encode('ascii'))
    token_digest = md5sum.digest()
    token_base64 = b64encode(token_digest).decode('ascii')
    
    # Perform URL-safe Base64 encoding
    token_formatted = token_base64.replace('\n', '').replace('+', '-').replace('/', '_').replace('=', '')
    
    return token_formatted

def encode_params(data):
    """Encode parameters for the URL."""
    result = []
    for k, vs in data.items():
        if isinstance(vs, str) or not hasattr(vs, "__iter__"):
            vs = [vs]
        for v in vs:
            if v is not None:
                result.append(
                    (
                        k.encode("utf-8") if isinstance(k, str) else k,
                        v.encode("utf-8") if isinstance(v, str) else v,
                    )
                )
    return urlencode(result, doseq=True)

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

        # Check if the path is already encoded
        if '%' not in url_path:
            url_path = quote(url_path)  # Ensure the path is properly encoded only if not already encoded
        
        # Calculate the expiration timestamp (e.g., 1 hour from now)
        expires = int(time.time()) + 3600
        
        # Generate the token using the security key, the extracted URL path, and expiration time
        token = generate_token(TOKEN_SECURITY_KEY, url_path, expires)
        
        # Add token and expiration to query parameters
        query_params = {
            "token": token,
            "expires": expires
        }

        # Concat the URL and query string
        options["url"] = f'{parsed_url.scheme}://{parsed_url.netloc}{url_path}?{encode_params(query_params)}'
    
    return options

# # Example usage
# options_1 = {"url": "https://test.b-cdn.net/Pt Alert-2.0.2.0.1.dmg"}
# processed_options_1 = process_request_options(options_1)
# print(f"Processed URL 1: {processed_options_1['url']}")

# options_2 = {"url": "https://example.com/assets/example_file.dmg"}
# processed_options_2 = process_request_options(options_2)
# print(f"Processed URL 2: {processed_options_2['url']}")
