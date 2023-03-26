$PLUGIN_DIRECTORY = "keypirinha-firefoxtabs"
$EXTENSION_NAME = "keypirinha-firefoxtabs.zip"
$PLUGIN_FILE = "FirefoxTabs.keypirinha-package"
$BUILD_DIRECTORY = "$PSScriptRoot/build"
$EXTENSION_FILE = "$BUILD_DIRECTORY/$EXTENSION_NAME"
$PLUGIN_ZIP = "$BUILD_DIRECTORY/FirefoxTabs.zip"
$PLUGIN_PATH = "$BUILD_DIRECTORY/$PLUGIN_FILE"

New-Item -ItemType Directory -Force -Path build | Out-Null
Remove-Item -Path "$BUILD_DIRECTORY/*"

# Build Firefox extension zip.
Compress-Archive -Path "./extension/*" -DestinationPath "$EXTENSION_FILE"
Write-Output "Firefox extension built at build/$EXTENSION_FILE."

Compress-Archive `
    -Path `
        "./$PLUGIN_DIRECTORY/src/firefoxtabs*",
        "./$PLUGIN_DIRECTORY/src/lib",
        "./$PLUGIN_DIRECTORY/LICENSE",
        "./$PLUGIN_DIRECTORY/README.md" `
    -DestinationPath "$PLUGIN_ZIP"
Move-Item -Path "$PLUGIN_ZIP" -Destination "$PLUGIN_PATH"
Write-Output "Keypirinha plugin built at build/$PLUGIN_FILE."
