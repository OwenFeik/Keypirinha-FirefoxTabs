$PLUGIN_NAME = "keypirinha-firefoxtabs"
$BUILD_DIRECTORY = "$PSScriptRoot/build"
$EXTENSION_FILE = "$BUILD_DIRECTORY/$PLUGIN_NAME.zip"
$PLUGIN_ZIP = "$BUILD_DIRECTORY/FirefoxTabs.zip"
$PLUGIN_FILE = "$BUILD_DIRECTORY/FirefoxTabs.keypirinha-package"

New-Item -ItemType Directory -Force -Path build
Remove-Item -Path "$BUILD_DIRECTORY/*"

Compress-Archive -Path "./extension/*" -DestinationPath "$EXTENSION_FILE"
Compress-Archive `
    -Path `
        "./$PLUGIN_NAME/src/firefoxtabs*",
        "./$PLUGIN_NAME/src/lib",
        "./$PLUGIN_NAME/LICENSE",
        "./$PLUGIN_NAME/README.md" `
    -DestinationPath "$PLUGIN_ZIP"
Move-Item -Path "$PLUGIN_ZIP" -Destination "$PLUGIN_FILE"
