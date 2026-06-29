from src.version import LATEST_RELEASE_URL, VERSION
from urllib.request import urlopen, urlretrieve
from packaging.version import Version
from dataclasses import dataclass
from pathlib import Path
import subprocess
import tempfile
import json
import sys
import os


@dataclass
class Release:
    version: str
    title: str
    body: str
    html_url: str
    download_url: str


def get_latest_release() -> Release | None:
    try:
        with urlopen(
            LATEST_RELEASE_URL,
            timeout=5,
        ) as response:
            data = json.load(response)
    except Exception:
        return None

    download_url = None
    for asset in data["assets"]:
        if asset["name"] == "GeradorDePastas.exe":
            download_url = asset["browser_download_url"]
            break

    return Release(
        version=data["tag_name"].removeprefix("v"),
        title=data["name"],
        body=data["body"],
        html_url=data["html_url"],
        download_url=download_url,
    )


def has_update() -> Release | None:
    release = get_latest_release()

    if release is None:
        return None

    if Version(release.version) <= Version(VERSION):
        return None

    return release


def update_program(self, release):
    if not getattr(sys, "frozen", False):
        return
    #
    # Baixa o novo executável
    #

    download_path = Path(tempfile.gettempdir()) / "GeradorReceitas.exe.new"

    urlretrieve(
        release.download_url,
        download_path,
    )

    #
    # Localiza o updater
    #

    updater_path = Path("updater.exe")

    #
    # Executa o updater
    #

    subprocess.Popen(
        [
            str(updater_path),
            str(os.getpid()),
            sys.executable,
            str(download_path),
        ],
        cwd=updater_path.parent,
    )

    #
    # Fecha o programa
    #

    self.destroy()
