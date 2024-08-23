# What is Bunny.net Middleware

Bunny.net Middleware enables munki managed clients to securely access a munki repo from Bunny's Global Content Delivery Network. 

Bunny.net Middleware uses a Bunny.net private key to create and sign requests for private Bunny.net resources. Each signed request includes an expiration date after which the request is no longer valid.

Bunny.net private keys are available from dash.bunny.ney > Delivery > CDN > Security > Token Authentication

## Requirements

* munki https://github.com/munki/munki
* Bunny.net pull zone with your munki repo inside. https://bunny.net?ref=mlmxq8squb
* Bunny.net Url Token Authentication Key for that pull zone

### Configure a managed client to access the Bunny.net munki repo

1. Install ```middleware_bunny.py``` to ```/usr/local/munki/```.
2. Set the munki preference ```SoftwareRepoURL``` (or ```PackageURL``` if you only serve the pkgs directory on bunny) to your Bunny.net Distribution URL.
3. Set Bunny.net Middleware preferences for your Access Key

    ```shell
    sudo defaults write /private/var/root/Library/Preferences/ManagedInstallsProc bunny_key "YOUR_BUNNY_KEY"
    ```

4. Run munki and verify that signed Bunny.net requests are being made.

    ```shell
    sudo managedsoftwareupdate --checkonly -vvv
    ```

## Packaging Bunny.net Middleware

The included luggage makefile can be used to create an installer package for Bunny.net Middleware.

1. ```make pkg``` and install.
2. Set your ```SoftwareRepoURL``` to your Bunny.net Distribution address and run munki.


