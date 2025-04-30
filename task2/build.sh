# any build steps,
# such as pip install, go build, etc
# should be run here to generate the pada executable
# do not run the executable here
SCRIPT_PATH="./pada.py"

pip install scapy

# Check if the script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: $SCRIPT_PATH not found."
    exit 1
fi

chmod +x "$SCRIPT_PATH"

cp "$SCRIPT_PATH" ./pada
chmod +x ./pada

# Confirm the 'pada' command works
echo "'pada' executable is now available in the current directory."


exit 0