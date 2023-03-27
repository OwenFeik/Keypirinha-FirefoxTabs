$BUILD_DIRECTORY = "$PSScriptRoot/build"             # Build output directory

$EXTENSION_NAME = "keypirinha-tabswitcher"           # Extension title
$EXTENSION_FILE = "$EXTENSION_NAME.zip"              # Extension file name
$EXTENSION_PATH = "$BUILD_DIRECTORY/$EXTENSION_FILE" # Extension file location

$PLUGIN_FILE = "FirefoxTabs.keypirinha-package"      # kp plugin file name
$PLUGIN_ZIP = "$BUILD_DIRECTORY/FirefoxTabs.zip"     # Intermediate file
$PLUGIN_PATH = "$BUILD_DIRECTORY/$PLUGIN_FILE"       # kp plugin file location

# Create build directory and delete any existing output files.
New-Item -ItemType Directory -Force -Path build | Out-Null
Remove-Item -Path "$BUILD_DIRECTORY/*"

# Build Firefox extension zip.
Compress-Archive -Path "./extension/*" -DestinationPath "$EXTENSION_PATH"
Write-Output "Firefox extension built at build/$EXTENSION_FILE."

# Build kp plugin and rename to appropriate extension.
Compress-Archive `
    -Path `
        "./src/firefoxtabs*",
        "./src/lib",
        "./LICENSE",
        "./README.md" `
    -DestinationPath "$PLUGIN_ZIP"
Move-Item -Path "$PLUGIN_ZIP" -Destination "$PLUGIN_PATH"
Write-Output "Keypirinha plugin built at build/$PLUGIN_FILE."
