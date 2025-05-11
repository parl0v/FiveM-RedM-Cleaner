import os
import sys
import subprocess
import time
import ctypes
import shutil
import psutil
import random
import socket
import winreg
from datetime import datetime
from tkinter import Tk, filedialog

ctypes.windll.kernel32.SetConsoleTitleW("A simple FiveM/RedM cleaner")

def print_start():
    os.system("cls")
    print("A simple FiveM/RedM cleaner")
    print("github.com/parl0v")
    print()
    print("This tool cleans traces and logs for FiveM and RedM")
    print()

def check_file_or_folder(path):
    return os.path.exists(os.path.expandvars(path))

def handle_remove_readonly(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def delete_file_or_folder(path):
    target = os.path.expandvars(path)
    if os.path.exists(target):
        try:
            if os.path.isdir(target):
                shutil.rmtree(target, onerror=handle_remove_readonly)
            else:
                try:
                    os.remove(target)
                except PermissionError:
                    os.chmod(target, stat.S_IWRITE)
                    os.remove(target)
        except Exception:
            pass

def terminate_process(process_name):
    try:
        subprocess.run(f"taskkill /f /im {process_name}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    except Exception as e:
        pass

def get_fivem_path():
    Tk().withdraw()
    fivem_path = filedialog.askopenfilename(title="Select FiveM.exe", filetypes=[("Executable Files", "*.exe")])
    if fivem_path and fivem_path.endswith("FiveM.exe"):
        return os.path.dirname(fivem_path)
    return None

def clean_fivem_files(fivem_base_path):
    if not fivem_base_path:
        print("FiveM path not provided.")
        return
    paths = [
        os.path.join(fivem_base_path, "FiveM.app", "logs"),
        os.path.join(fivem_base_path, "FiveM.app", "crashes"),
        os.path.join(fivem_base_path, "FiveM.app", "data")
    ]
    for path in paths:
        delete_file_or_folder(path)
    print("FiveM files cleaned successfully.")

def get_redm_path():
    Tk().withdraw()
    redm_path = filedialog.askopenfilename(title="Select RedM.exe", filetypes=[("Executable Files", "*.exe")])
    if redm_path and redm_path.endswith("RedM.exe"):
        return os.path.dirname(redm_path)
    return None

def clean_redm_files(redm_base_path):
    if not redm_base_path:
        print("RedM path not provided.")
        return
    paths = [
        os.path.join(redm_base_path, "RedM.app", "logs"),
        os.path.join(redm_base_path, "RedM.app", "crashes"),
        os.path.join(redm_base_path, "RedM.app", "data")
    ]
    for path in paths:
        delete_file_or_folder(path)
    print("RedM files cleaned successfully.")

def clean_appdata():
    appdata = os.getenv("APPDATA")
    citizenfx = os.path.join(appdata, "CitizenFX")
    if os.path.exists(citizenfx):
        for name in os.listdir(citizenfx):
            delete_file_or_folder(os.path.join(citizenfx, name))
            
    local_appdata = os.getenv("LOCALAPPDATA")
    digital_entitlements = os.path.join(local_appdata, "DigitalEntitlements")
    delete_file_or_folder(digital_entitlements)

    print("AppData cleaned successfully.")

def clean_temp_files():
    local_appdata = os.getenv("LOCALAPPDATA")
    temp = os.path.join(local_appdata, "Temp")
    delete_file_or_folder(temp)
    crash = os.path.join(local_appdata, "CrashDumps")
    delete_file_or_folder(crash)

def clean_windows_temp():
    temp = os.path.join(os.getenv("SYSTEMROOT"), "Temp")
    delete_file_or_folder(temp)

def clean_prefetch():
    prefetch = os.path.join(os.getenv("SYSTEMROOT"), "Prefetch")
    delete_file_or_folder(prefetch)

def clean_microsoft():
    temp = os.path.join(os.getenv("PROGRAMDATA"), "Microsoft", "Windows", "WER", "ReportArchive")
    delete_file_or_folder(temp)

def clean_steam():
    paths = [
        os.path.join(os.getenv("LOCALAPPDATA"), "Temp"),
        os.path.join(os.getenv("LOCALAPPDATA"), "CrashDumps"),
        os.path.join(os.getenv("WINDIR"), "Temp"),
        os.path.join(os.getenv("WINDIR"), "Prefetch"),
        os.path.join(os.getenv("PROGRAMDATA"), "Microsoft", "Windows", "WER", "ReportArchive"),
        os.path.join(os.getenv("LOCALAPPDATA"), "Steam", "htmlcache"),
        os.path.join(os.getenv("PROGRAMFILES(x86)"), "Steam", "config", "loginusers.vdf")
    ]
    for path in paths:
        delete_file_or_folder(path)

def delete_key_recursive(root, subkey):
    try:
        with winreg.OpenKey(root, subkey, 0, winreg.KEY_ALL_ACCESS) as key:
            i = 0
            while True:
                try:
                    sub = winreg.EnumKey(key, i)
                    delete_key_recursive(root, f"{subkey}\\{sub}")
                    i += 1
                except OSError:
                    break
        winreg.DeleteKey(root, subkey)
    except Exception:
        pass

def remove_xbox_registry_keys():
    keys = [
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\UserData\UninstallTimes"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes\Local Settings\MrtCache"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppContainer\Storage\microsoft.xboxgamingoverlay_8wekyb3d8bbwe"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\Repository\Packages\Microsoft.XboxGamingOverlay_7.224.11211.0_x64__8wekyb3d8bbwe"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\SystemAppData\Microsoft.XboxGamingOverlay_8wekyb3d8bbwe"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\PackageRepository\Packages\Microsoft.XboxGamingOverlay_7.224.11211.0_neutral_~_8wekyb3d8bbwe"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\PackageRepository\Packages\Microsoft.XboxGamingOverlay_7.224.11211.0_x64__8wekyb3d8bbwe"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\PackageRepository\Packages\Microsoft.XboxGamingOverlay_7.224.11211.0_neutral_split.language-th_8wekyb3d8bbwe"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Xbox"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Xbox"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\XblAuthManager"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\XblGameSave"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\XboxNetApiSvc"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\GamingServices"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI\Xbox"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI\Xbox"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\GameBar"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\GameBar"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\GameBarPresenceWriter"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\Microsoft.XboxGamingOverlay.exe"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\Microsoft.XboxGamingOverlay.exe")
    ]
    for rootkey, key_path in keys:
        try:
            winreg.DeleteKey(rootkey, key_path)
        except Exception:
            try:
                key = winreg.OpenKey(rootkey, key_path, 0, winreg.KEY_ALL_ACCESS)
                delete_key_recursive(key, "")
                winreg.CloseKey(key)
            except Exception:
                pass

def remove_xbox_apps():
    xbox_apps = [
        "Microsoft.XboxApp", "Microsoft.XboxGameOverlay", "Microsoft.XboxGamingOverlay",
        "Microsoft.XboxSpeechToTextOverlay", "Microsoft.XboxIdentityProvider", "Microsoft.Xbox.TCUI",
        "Microsoft.XboxGameCallableUI", "Microsoft.GamingServices", "Microsoft.GamingApp"
    ]
    for app in xbox_apps:
        try:
            subprocess.run(["powershell", "-Command", f"Get-AppxPackage *{app}* | Remove-AppxPackage -AllUsers"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, shell=True)
        except subprocess.CalledProcessError:
            pass
    clear_xbox_services()

def clear_xbox_services():
    try:
        subprocess.run(["powershell", "-Command", "Get-Service Xbox* | Stop-Service -Force"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, shell=True)
        subprocess.run(["powershell", "-Command", "Get-Service Xbox* | Set-Service -StartupType Disabled"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, shell=True)
        print_start()
        print("Xbox services disabled and stopped.")
        remove_xbox_registry_keys()
        remove_xbox_traces()
    except subprocess.CalledProcessError:
        pass

def remove_xbox_traces():
    xbox_folders = [
        os.path.join(os.getenv("LOCALAPPDATA"), "Packages", "Microsoft.Xbox*"),
        os.path.join(os.getenv("PROGRAMFILES"), "ModifiableWindowsApps"),
        os.path.join(os.getenv("SYSTEMDRIVE"), "Program Files", "WindowsApps", "Microsoft.Xbox*"),
        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "XboxLive"),
        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "XboxIdentityProvider"),
        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "XboxSpeechToTextOverlay"),
        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "XboxGameOverlay"),
        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "XboxGamingOverlay"),
        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "XboxApp")
    ]
    for folder in xbox_folders:
        try:
            delete_file_or_folder(folder)
        except Exception as e:
            pass

def generate_random_mac():
    return ":".join("{:02x}".format(random.randint(0, 255)) for _ in range(6))

def spoof_mac_address():
    adapters = [name for name in psutil.net_if_addrs() if name.lower() != "loopback"]
    if not adapters:
        print_start()
        print("No network adapters found.")
        return

    for adapter in adapters:
        new_mac = generate_random_mac().replace(":", "")
        try:
            command = f"Get-NetAdapter -Name '{adapter}' | Set-NetAdapterAdvancedProperty -RegistryKeyword 'NetworkAddress' -RegistryValue '{new_mac}'"
            subprocess.run(["powershell", "-Command", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, shell=True)
            subprocess.run(["powershell", "-Command", f"Disable-NetAdapter -Name '{adapter}' -Confirm:$false"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, shell=True)
            time.sleep(2)
            subprocess.run(["powershell", "-Command", f"Enable-NetAdapter -Name '{adapter}'"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, shell=True)
        except Exception as e:
            pass

def ask_mac_spoofing():
    choice = input("Would you like to spoof your MAC address for every adapter? [y/n]: ").strip().lower()
    if choice == "y":
        print_start()
        print("Spoofing...")
        spoof_mac_address()

def get_adapter_name():
    for interface in psutil.net_if_addrs():
        if interface.lower() != "loopback" and interface:
            return interface
    return None

def network_reset():
    adapter_name = get_adapter_name()
    if not adapter_name:
        print_start()
        print("No active network adapter found.")
    else:
        try:
            subprocess.run("ipconfig /release", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            time.sleep(2)
            subprocess.run("ipconfig /renew", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            print_start()
            print("Network adapter reset successfully.")
        except Exception as e:
            print_start()
            print("Network reset failed.")

def ask_to_unlink_rockstar():
    print("Unlink Rockstar? [y/n]")
    choice = input().strip()
    if choice == "y":
        print_start()
        print("Unlinking Rockstar...")
        clean_appdata()
    else:
        print_start()
        print("Skipping Rockstar unlinking...")
        time.sleep(2)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def run_as_admin():
    script = os.path.abspath(__file__)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}"', None, 1)

def show_admin_warning():
    ctypes.windll.user32.MessageBoxW(0, "Restarting as admin.", "Administrative Privileges Required", 262160)

def main():
    if not is_admin():
        show_admin_warning()
        run_as_admin()
        sys.exit()

    print_start()
    time.sleep(1)
    input("Press ENTER to start the cleaner...\n")
    
    print_start()
    
    print("Blocking traces...")
    time.sleep(2)
    common_processes = [
        "steam.exe", "steamwebhelper.exe", "steamservice.exe",
        "FiveM.exe", "FiveM_Diag.exe", "FiveM_ChromeBrowser.exe",
        "FiveM_ROSLauncher.exe", "FiveM_ROSService.exe",
        "RedM.exe", "RedM_Diag.exe", "RedM_ChromeBrowser.exe",
        "RedM_ROSLauncher.exe", "RedM_ROSService.exe"
    ]
    for proc in common_processes:
        terminate_process(proc)
    
    print_start()
    
    ask_mac_spoofing()
    print_start()
    print("Network Reset...")
    time.sleep(2)
    network_reset()
    time.sleep(2)
    print_start()
    
    ask_to_unlink_rockstar()
    time.sleep(2)
    print_start()
    
    print("Cleaning Xbox traces and apps...")
    remove_xbox_apps()
    time.sleep(2)
    print_start()
    
    choice = input("Do you want to clean FiveM traces? [y/n]: ").lower().strip()
    if choice == "y":
        print_start()
        fivem_base_path = get_fivem_path()
        if fivem_base_path:
            time.sleep(2)
            clean_fivem_files(fivem_base_path)
            print("FiveM traces cleaned.")
        else:
            print("FiveM path not provided. Skipping FiveM cleaning.")
    else:
        print_start()
        print("Skipping FiveM cleaning.")
    time.sleep(2)
    print_start()
    
    choice = input("Do you want to clean RedM traces? [y/n]: ").lower().strip()
    if choice == "y":
        print_start()
        redm_base_path = get_redm_path()
        if redm_base_path:
            time.sleep(2)
            clean_redm_files(redm_base_path)
            print("RedM traces cleaned.")
        else:
            print("RedM path not provided. Skipping RedM cleaning.")
    else:
        print_start()
        print("Skipping RedM cleaning.")
    time.sleep(2)
    
    print_start()
    
    print("Cleaning Temp Files...")
    time.sleep(2)
    clean_temp_files()
    clean_prefetch()
    clean_windows_temp()
    clean_microsoft()
    clean_steam()
    time.sleep(2)
    print_start()
    
    print("Cleaning complete.")
    time.sleep(2)
    input("\nPress ENTER to exit...")
    time.sleep(1)
    sys.exit()

if __name__ == "__main__":
    os.system("cls")
    main()