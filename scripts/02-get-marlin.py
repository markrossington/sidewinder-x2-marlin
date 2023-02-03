import os
import shutil
import urllib.request
import zipfile

repository_root = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
requested_version = input("Enter which version to download, blank will get latest: ")
bugfix = "bugfix-"

if requested_version == "":
    download_version = "2.1.x"
else:
    download_version = requested_version

marlin_download_url = (
    f"https://github.com/MarlinFirmware/Marlin/archive/{bugfix}{download_version}.zip"
)
download_zip_filepath = f"tmp/marlin_{download_version}.zip"

os.chdir(repository_root)

print("Making tmp amd build dir")
os.makedirs("tmp", exist_ok=True)
os.makedirs("build", exist_ok=True)

print(
    f"Downloading version {download_version} from {marlin_download_url} to {download_zip_filepath}..."
)
urllib.request.urlretrieve(marlin_download_url, download_zip_filepath)

print("Deleting existing in build directory")
shutil.rmtree("build")
os.makedirs("build", exist_ok=True)

print(f"Extracting {download_zip_filepath} to build folder...")
with zipfile.ZipFile(download_zip_filepath, "r") as zip_ref:
    zip_ref.extractall("build")

print(f"Cleaning up {download_zip_filepath}")
os.remove(download_zip_filepath)
