# Keypirinha Plugin: FirefoxTabs

This is FirefoxTabs, a plugin for the
[Keypirinha](http://keypirinha.com) launcher.

FirefoxTabs, in combination with the provided Firefox extension, adds, as the
name suggests, Firefox tabs as suggestions in Keypirinha.


## Download

https://github.com/OwenFeik/fftabs/releases


## Install

* Once you've downloaded `FirefoxTabs.keypirinha-package`, move it to the
`InstalledPackage` folder located at:
    * `Keypirinha\portable\Profile\InstalledPackages` in **Portable mode**
    * **Or** `%APPDATA%\Keypirinha\InstalledPackages` in **Installed mode**
        (the final path would look like 
        `C:\Users\%USERNAME%\AppData\Roaming\Keypirinha\InstalledPackages`)

* Then, install the Firefox extension located at `/extension`, to switch to
    tabs when Firefox is launched by FirefoxTabs.

FirefoxTabs requires [`lz4`](https://github.com/lz4/lz4/releases). It is able
to install it automatically, and will do so when launched. If it does so, the
file will be placed in `%APPDATA%\Keypirinha\PackageData\FirefoxTabs`. However,
if the `lz4` command is found in `PATH`, FirefoxTabs will check for an already
installed DLL first.

## Usage

Once installed, FirefoxTabs should automatically pick up existing sessions and
start suggesting tabs from them. You can search on tab name or URL. If a new
session is created, you'll need to reload the catalog for suggestions to start
appearing from it.

## License

This package is distributed under the terms of the MIT license.
