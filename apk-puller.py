import subprocess
import os


def get_apk_paths(package_name):
    """Get the list of APK paths for the given package name."""
    try:
        result = subprocess.run(
            ["adb", "shell", "pm", "path", package_name],
            capture_output=True,
            text=True,
            check=True
        )
        apk_paths = result.stdout.splitlines()
        apk_paths = [line.split(":")[1] for line in apk_paths if line.startswith("package:")]
        return apk_paths
    except subprocess.CalledProcessError as e:
        print(f"Error getting APK paths: {e}")
        return []


def pull_apk_files(apk_paths, dest_dir):
    """Pull APK files from the device to the local directory."""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for apk_path in apk_paths:
        apk_name = os.path.basename(apk_path)
        local_path = os.path.join(dest_dir, apk_name)
        try:
            subprocess.run(
                ["adb", "pull", apk_path, local_path],
                check=True
            )
            print(f"Pulled {apk_name} to {local_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error pulling {apk_path}: {e}")


def main():
    package_name = input("Enter the package name: ")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, package_name)

    apk_paths = get_apk_paths(package_name)

    if not apk_paths:
        print(f"No APK paths found for package: {package_name}")
        return

    pull_apk_files(apk_paths, dest_dir)
    print("Finished pulling APKs.")


if __name__ == "__main__":
    main()
