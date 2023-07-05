# APK Decompiling & Signing Script

This script allows you to decompile an APK file, modify it, and then sign it using the Android SDK tools.

## Prerequisites

- [APKTool](https://ibotpeaches.github.io/Apktool/) installed. You can install it using Homebrew:

    ```bash
    brew install apktool
    ```

- [Android SDK](https://developer.android.com/studio#downloads) installed and the `ANDROID_SDK_ROOT` environment variable set. If the environment variable is not set, you will be prompted to enter the path to the Android SDK directory when running the script.

- Python 3.11.4 or compatible version installed.

## Tested Environment

The APK Signing Script has been tested on the following environment:

- macOS Ventura 13.4
- Android SDK 29.0.2
- Python 3.11.4

## Usage

1. Clone or download the script.

2. Install the prerequisites mentioned above.

3. Open a terminal and navigate to the directory where the script is located.

4. Run the script using the following command:

    ```bash
    python3 apk_signer.py
    ```

5. Follow the prompts to provide the necessary information such as the APK file path, build version, keystore file path, alias, and password.

6. The script will decompile the APK, prompt you to modify the original APK, rebuild the decompiled APK, and sign it using the provided keystore file.

7. The signed APK will be generated in the same directory as the decompiled APK.

## License

This script is released under the [MIT License](LICENSE).
