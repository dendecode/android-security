import os
import subprocess
import shutil
import getpass
import tempfile
import time

# Check if apktool is installed
if not shutil.which('apktool'):
    install_apktool = input("APKTool is not found. Do you want to install it using Homebrew? (y/n): ")
    if install_apktool.lower() == 'y':
        print("Installing APKTool using Homebrew...")
        subprocess.run(['brew', 'install', 'apktool'])
        print("APKTool is now installed.")
    else:
        print("APKTool is required but not installed. Exiting...")
        exit(1)

# Find the root path of the Android SDK
ANDROID_SDK_ROOT = ''
if os.path.isdir('/usr/local/Caskroom/android-sdk'):
    ANDROID_SDK_ROOT = '/usr/local/Caskroom/android-sdk'
elif os.path.isdir(os.path.join(os.environ['HOME'], 'Library/Android/sdk')):
    ANDROID_SDK_ROOT = os.path.join(os.environ['HOME'], 'Library/Android/sdk')
elif os.path.isdir('/usr/local/opt/android-sdk'):
    ANDROID_SDK_ROOT = '/usr/local/opt/android-sdk'

# Prompt the user to enter the Android SDK root path if not found
if not ANDROID_SDK_ROOT:
    ANDROID_SDK = input("Enter the path to the Android SDK directory: ")
else:
    print("Android SDK found at:", ANDROID_SDK_ROOT)
    sdk_correct_path = input("Is this the correct path? (y/n): ")
    if sdk_correct_path.lower() == 'y':
        ANDROID_SDK = ANDROID_SDK_ROOT
    else:
        ANDROID_SDK = input("Enter the path to the Android SDK directory: ")

# List available build versions
build_tools_dir = os.path.join(ANDROID_SDK, 'build-tools')
build_versions = [d for d in os.listdir(build_tools_dir) if os.path.isdir(os.path.join(build_tools_dir, d))]
print("Available build versions:")
for i, version in enumerate(build_versions, 1):
    print(f"{i}. {version}")

# Prompt for the Android build version
build_version_choice = input("Do you want to use the last available build version? (y/n): ")
if build_version_choice.lower() == 'y':
    BUILD_VERSION = build_versions[-1]
else:
    print("Choose a build version from the list (enter the corresponding number):")
    build_version_index = int(input())
    while build_version_index < 1 or build_version_index > len(build_versions):
        print("Invalid choice. Please choose a valid number.")
        build_version_index = int(input())
    BUILD_VERSION = build_versions[build_version_index - 1]

# Prompt for the path to the keystore file or use the default one
KEYSTORE_FILE = input("Enter the path to the keystore file (or leave empty to use the default): ")
if not KEYSTORE_FILE:
    # Set the path to the default keystore file (key.keystore in the same folder as the script)
    KEYSTORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'key.keystore')
    KEY_ALIAS = "alias_name"
    KEY_PASSWORD = "ciaobello"
else:
    KEY_ALIAS = input("Enter the alias of the key in the keystore: ")
    KEY_PASSWORD = getpass.getpass("Enter the key password: ")

# Prompt for the path to the APK file
APK_FILE = input("Enter the path to the APK file to reverse: ")

# Set the output directory for the decompiled APK files
OUTPUT_DIR = os.path.join(os.path.dirname(APK_FILE), 'decompiled')

# Create the output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Display the loader while decompiling the APK
print("Decompiling")
with tempfile.TemporaryFile() as tempf:
    proc = subprocess.Popen(['apktool', 'd', '-f', APK_FILE, '-o', OUTPUT_DIR], stdout=tempf)
    while proc.poll() is None:
        print(".", end="", flush=True)
        time.sleep(0.5)

print("\nDecompiling process completed.")

# Prompt to modify the original APK
input("Waiting to modify the original APK (/decompiled folder). Once you're finished, press ENTER to REBUILD and SIGN the decompiled/reversed APK...")

# Display the loader while rebuilding the APK
print("Rebuilding")
with tempfile.TemporaryFile() as tempf:
    proc = subprocess.Popen(['apktool', 'b', '-o', os.path.join(OUTPUT_DIR, 'rebuild.apk'), OUTPUT_DIR], stdout=tempf)
    while proc.poll() is None:
        print(".", end="", flush=True)
        time.sleep(0.5)

print("\nRebuilding process completed.")

# Sign the decompiled APK if a signing key is provided
if os.path.isfile(KEYSTORE_FILE) and KEY_PASSWORD:
    # Align the decompiled APK using zipalign
    subprocess.run([os.path.join(ANDROID_SDK, 'build-tools', BUILD_VERSION, 'zipalign'), '-v', '4',
                    os.path.join(OUTPUT_DIR, 'rebuild.apk'),
                    os.path.join(OUTPUT_DIR, 'aligned.apk')])

    # Display the loader while signing the APK
    print("Signing")
    with tempfile.TemporaryFile() as tempf:
        proc = subprocess.Popen([os.path.join(ANDROID_SDK, 'build-tools', BUILD_VERSION, 'apksigner'), 'sign',
                                 '--ks', KEYSTORE_FILE, '--ks-pass', 'pass:' + KEY_PASSWORD,
                                 '--out', os.path.join(OUTPUT_DIR, 'signed.apk'),
                                 os.path.join(OUTPUT_DIR, 'aligned.apk')], stdout=tempf)
        while proc.poll() is None:
            print(".", end="", flush=True)
            time.sleep(0.5)

    print("\nAPK signing process COMPLETED.")

    # Verify the APK signature
    subprocess.run([os.path.join(ANDROID_SDK, 'build-tools', BUILD_VERSION, 'apksigner'), 'verify', '--verbose',
                    os.path.join(OUTPUT_DIR, 'signed.apk')])
    print("\nAPK verify process COMPLETED.")

else:
    print("Skipping signing. No signing key provided.")
