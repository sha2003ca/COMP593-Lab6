import hashlib
import os
import requests


def main():
    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):
        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)


def get_expected_sha256():
    url = "https://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.7z.sha256"
    response = requests.get(url)
    return response.text.strip().split()[0]


def download_installer():
    url = "http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.7z"
    response = requests.get(url)
    return response.content


def installer_ok(installer_data, expected_sha256):
    sha256 = hashlib.sha256(installer_data).hexdigest()
    return sha256 == expected_sha256


def save_installer(installer_data):
    temp_folder = os.getenv('TEMP')
    installer_path = os.path.join(temp_folder, "vlc_installer.7z")
    with open(installer_path, "wb") as f:
        f.write(installer_data)
    return installer_path


def run_installer(installer_path):
    cmd = f'{installer_path} /S'
    os.system(cmd)


def delete_installer(installer_path):
    os.remove(installer_path)


if __name__ == '__main__':
    main()