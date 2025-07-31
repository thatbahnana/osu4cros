#!/usr/bin/python3
import os
import shutil
import subprocess
import platform
import requests

USER_PATH = os.path.expanduser("~")
LATEST_OSU_APPIMG = "https://github.com/ppy/osu/releases/latest/download/osu.AppImage"
OSU_APPUMG_NAME = "osu.AppImage"
OSU_ROOTNAME = "osu-lazer"

def is_chromebook() -> bool:
    return subprocess.check_output(
        [
            "cat",
            "/sys/class/dmi/id/product_name"
        ],
        text=True
    ).strip() == "crosvm"

def is_crostini() -> bool:
    return platform.freedesktop_os_release()['ID'] == "debian" and is_chromebook()

def is_executable(file_path: os.PathLike) -> bool:
    return os.access(file_path, os.X_OK)

def make_executable(file_path: os.PathLike) -> None:    
    os.chmod(file_path, 0o755)

def hyperlink(label: str, url: requests.URLRequired) -> str:
    return f"\033]8;;{url}\033\\{label}\033]8;;\033\\"

def divide_by_coeff(amount: int, coeff: int) -> int | float:
    return amount / coeff

def octets_to_mo(amount: int) -> int | float:
    return divide_by_coeff(amount=amount, coeff=1048576)

def create_file(content: str, path: os.PathLike) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as file:
        file.write(content)

def download(url: str, file_path: os.PathLike, allow_overwrite: bool = False) -> None:    
    if not allow_overwrite and os.path.exists(file_path):
        raise FileExistsError(f"The file '{file_path}' already exists.")
     
    response = requests.get(url, stream=True)
    
    total_size = int(response.headers.get('content-length', 0))
    downloaded_size = 0

    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):    
            file.write(chunk)
            downloaded_size += len(chunk)
            print(f"[{round(octets_to_mo(downloaded_size))}/{round(octets_to_mo(total_size))}Mo] Downloading '{os.path.basename(file_path)}' at '{url}'...", end="\r")
            
    print("\nDone!\n")

def install_appimage(
    appimage_path: os.PathLike,
    install_path: os.PathLike | None = None,
    rootname: str | None = None,
    # Do not change "default_rootname" exept if you know what you're doing !
    default_rootname: str = "squashfs-root") -> None:
    
    # Give install_path a default value if not provided
    if install_path is None: 
        install_path = os.getcwd()
    
    # Give rootname a default value if not provided
    if rootname is None:
        rootname = os.path.splitext(os.path.basename(appimage_path))[0]
    
    # Make sure the AppImage is executable and make it executable if not
    if not is_executable(appimage_path):
        make_executable(appimage_path)
    
    print(f"Installing '{appimage_path}' in '{__name__ if install_path is None else install_path}' as '{rootname}'...")     
    subprocess.run(
        [
            appimage_path,
            "--appimage-extract"
        ],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        check=True
    )
    
    # Remove potential old installation
    if os.path.exists(f"{install_path}/{rootname}"):
        shutil.rmtree(f"{install_path}/{rootname}")
    
    # Rename default rootname to the specified rootname
    os.rename(default_rootname, rootname)
    
    # Move the extracted files to the install path dosn't exist
    if not os.path.exists(install_path):
        shutil.move(rootname, install_path)
     
    print("Done!\n")

def main():
    print("Welcome to 'osu4cros', probably the only osu!(lazer) installer for ChromeOS devices. (Press Ctrl + C to exit)...")
    input("Hit 'Enter' to install osu! (lazer)...\n")
    
    print("Verifying system integrity...")
    if not is_chromebook():
        print(f"This script was designed to run on a ChromeOS device. Please run on a proper device.")
        exit(1)
    
    if is_crostini():
        print(f"""
This script is designed to run exclusively within the Steam environment (Borealis).
Please {hyperlink(label='visit the list of devices compatible with Steam (Borealis)', url='https://www.exemple.com/')}.""")
        exit(1)
    print("Done!\n")
    
    download(
        LATEST_OSU_APPIMG,
        f"{USER_PATH}/{OSU_APPUMG_NAME}",
        allow_overwrite=True
    )
    install_appimage(
        appimage_path=f"{USER_PATH}/{OSU_APPUMG_NAME}",
        install_path=USER_PATH,
        rootname=OSU_ROOTNAME
    )

    print("Creating desktop entry...")
    create_file(f"""\
# Desktop Entry Specification: https://standards.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html
[Desktop Entry]

Version=1.5
Type=Application
Name=osu!(lazer)
Comment=A free-to-win rhythm game. Rhythm is just a *click* away!
Icon={USER_PATH}/{OSU_ROOTNAME}/usr/share/icons/hicolor/256x256/apps/osu.png
Exec={USER_PATH}/{OSU_ROOTNAME}/AppRun
Terminal=false
MimeType=application/x-osu-beatmap-archive;application/x-osu-skin-archive;application/x-osu-beatmap;application/x-osu-storyboard;application/x-osu-replay;x-scheme-handler/osu;
Categories=Game;
StartupWMClass=osu!
SingleMainWindow=true
StartupNotify=true""",
    f"{USER_PATH}/.local/share/applications/osu-lazer.desktop")
    print("Done!\n")
      
    print("""\
Thank you for using 'osu4cros'! You can launch 'osu!' from the App Launcher.
Don't forget to apply the recommended settings when launching the game!

Have fun <3
""")
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSee you next time! ^^")
