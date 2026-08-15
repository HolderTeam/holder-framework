#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone
from pathlib import Path

import biplist
import ds_store
import mac_alias


WINDOW_BOUNDS = "{{100, 100}, {640, 480}}"
HOLDER_ICON_LOCATION = (192, 328)
APPLICATIONS_ICON_LOCATION = (448, 328)
HIDDEN_ICON_LOCATION = (620, 440)


def create_alias(volume_name: str, filename: str) -> mac_alias.Alias:
    now = datetime.now(timezone.utc)
    volume = mac_alias.VolumeInfo(
        volume_name,
        now,
        fs_type=mac_alias.ALIAS_HFS_VOLUME_SIGNATURE,
        disk_type=mac_alias.ALIAS_FIXED_DISK,
        attribute_flags=0,
        fs_id=bytes(2),
    )
    target = mac_alias.TargetInfo(
        mac_alias.ALIAS_KIND_FILE,
        filename,
        folder_cnid=0,
        cnid=0,
        creation_date=now,
        creator_code=bytes(4),
        type_code=bytes(4),
        folder_name=volume_name,
        carbon_path=f"{volume_name}:{filename}",
    )
    return mac_alias.Alias(volume=volume, target=target)


def main() -> None:
    parser = argparse.ArgumentParser(description="Write Holder DMG Finder layout metadata.")
    parser.add_argument("--mount", required=True, help="Mounted DMG volume path")
    parser.add_argument("--volume-name", required=True, help="DMG volume name")
    args = parser.parse_args()

    mount_path = Path(args.mount)
    ds_store_path = mount_path / ".DS_Store"

    icon_view = {
        "backgroundType": 2,
        "backgroundColorRed": 1.0,
        "backgroundColorGreen": 1.0,
        "backgroundColorBlue": 1.0,
        "backgroundImageAlias": biplist.Data(
            create_alias(args.volume_name, ".background.png").to_bytes()
        ),
        "viewOptionsVersion": 1,
        "gridSpacing": 100.0,
        "gridOffsetX": 0.0,
        "gridOffsetY": 0.0,
        "scrollPositionY": 0.0,
        "arrangeBy": "none",
        "labelOnBottom": True,
        "showItemInfo": False,
        "showIconPreview": True,
        "iconSize": 96.0,
        "textSize": 14.0,
    }

    window = {
        "WindowBounds": WINDOW_BOUNDS,
        "ShowToolbar": False,
        "ShowPathbar": False,
        "ShowStatusBar": False,
    }

    store = ds_store.DSStore.open(str(ds_store_path), "w+")
    try:
        store["."]["vSrn"] = ("long", 1)
        store["."]["icvl"] = ("type", "icnv")
        store["."]["icvp"] = icon_view
        store["."]["bwsp"] = window
        store["Holder.app"]["Iloc"] = HOLDER_ICON_LOCATION
        store["Applications"]["Iloc"] = APPLICATIONS_ICON_LOCATION
        store[".background.png"]["Iloc"] = HIDDEN_ICON_LOCATION
        store[".fseventsd"]["Iloc"] = HIDDEN_ICON_LOCATION
    finally:
        store.close()


if __name__ == "__main__":
    main()
