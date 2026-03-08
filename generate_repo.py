#!/usr/bin/env python3
"""
Generate Kodi repository files: addons.xml and addons.xml.md5
Run this script after updating any addon to regenerate the repo index.
"""
import os
import hashlib
import xml.etree.ElementTree as ET
import shutil
import zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ZIPS_DIR = os.path.join(SCRIPT_DIR, 'zips')
ADDON_SOURCE = os.path.join(SCRIPT_DIR, '..', 'plugin.video.cricket.live')
REPO_SOURCE = os.path.join(SCRIPT_DIR, 'repository.myatv')

def zip_addon(source_dir, dest_dir):
    """Create a zip of the addon in the zips directory."""
    addon_id = os.path.basename(source_dir)
    tree = ET.parse(os.path.join(source_dir, 'addon.xml'))
    version = tree.getroot().get('version')

    zip_dir = os.path.join(dest_dir, addon_id)
    os.makedirs(zip_dir, exist_ok=True)

    zip_path = os.path.join(zip_dir, f'{addon_id}-{version}.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source_dir):
            for f in files:
                filepath = os.path.join(root, f)
                arcname = os.path.join(addon_id, os.path.relpath(filepath, source_dir))
                zf.write(filepath, arcname)

    print(f'  Zipped: {addon_id} v{version} -> {os.path.basename(zip_path)}')
    return addon_id

def generate_addons_xml():
    """Generate addons.xml from all addon.xml files."""
    addons_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addons>\n'

    addon_dirs = [ADDON_SOURCE, REPO_SOURCE]

    for addon_dir in addon_dirs:
        addon_xml_path = os.path.join(addon_dir, 'addon.xml')
        if not os.path.exists(addon_xml_path):
            continue

        with open(addon_xml_path, 'r') as f:
            content = f.read().strip()

        # Remove XML declaration if present
        if content.startswith('<?xml'):
            content = content.split('?>', 1)[1].strip()

        addons_xml += content + '\n\n'

    addons_xml += '</addons>\n'
    return addons_xml

def generate_md5(content):
    """Generate MD5 hash of content."""
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def main():
    print('MyATV Kodi Repository Generator')
    print('=' * 40)

    # Step 1: Zip addons
    print('\n1. Creating addon zips...')
    zip_addon(ADDON_SOURCE, ZIPS_DIR)
    zip_addon(REPO_SOURCE, ZIPS_DIR)

    # Step 2: Generate addons.xml
    print('\n2. Generating addons.xml...')
    addons_xml = generate_addons_xml()
    addons_xml_path = os.path.join(ZIPS_DIR, 'addons.xml')
    with open(addons_xml_path, 'w') as f:
        f.write(addons_xml)
    print(f'  Written: {addons_xml_path}')

    # Step 3: Generate MD5
    print('\n3. Generating addons.xml.md5...')
    md5 = generate_md5(addons_xml)
    md5_path = os.path.join(ZIPS_DIR, 'addons.xml.md5')
    with open(md5_path, 'w') as f:
        f.write(md5)
    print(f'  MD5: {md5}')

    # Step 4: Create root installer zip (for initial install from zip)
    print('\n4. Creating repository installer zip...')
    installer_zip = os.path.join(SCRIPT_DIR, 'repository.myatv.zip')
    with zipfile.ZipFile(installer_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(REPO_SOURCE):
            for f in files:
                filepath = os.path.join(root, f)
                arcname = os.path.join('repository.myatv', os.path.relpath(filepath, REPO_SOURCE))
                zf.write(filepath, arcname)
    print(f'  Written: {installer_zip}')

    print('\n' + '=' * 40)
    print('Done! Repository files generated.')
    print(f'\nFiles in zips/:')
    for root, dirs, files in os.walk(ZIPS_DIR):
        for f in files:
            path = os.path.join(root, f)
            size = os.path.getsize(path)
            print(f'  {os.path.relpath(path, ZIPS_DIR)} ({size:,} bytes)')

if __name__ == '__main__':
    main()
