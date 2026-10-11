"""Run inside the Odoo container. This script prints no credentials."""
import ast
import configparser
import json
from pathlib import Path
import sys

import odoo
import odoo.addons
from odoo import release

REQUIRED = ['contacts', 'stock', 'purchase', 'sale_management', 'mrp', 'project']
BRIDGES = ['purchase_stock', 'sale_stock']
roots = [Path(p) for p in getattr(odoo.addons, '__path__', [])]
if getattr(odoo, '__file__', None):
    roots.append(Path(odoo.__file__).resolve().parent / 'addons')
for p in getattr(odoo, '__path__', []):
    roots.append(Path(p) / 'addons')
    roots.append(Path(p).resolve().parent / 'addons')
config = configparser.ConfigParser()
config.read('/etc/odoo/odoo.conf')
for part in config.get('options', 'addons_path', fallback='').split(','):
    if part.strip():
        roots.append(Path(part.strip()))
roots = list(dict.fromkeys(p.resolve() for p in roots))
modules = {}
for name in REQUIRED + BRIDGES:
    path = next((p / name / '__manifest__.py' for p in roots if (p / name / '__manifest__.py').is_file()), None)
    if path is None:
        modules[name] = {'found': False}
        continue
    manifest = ast.literal_eval(path.read_text(encoding='utf-8'))
    modules[name] = {
        'found': True,
        'name': manifest.get('name'),
        'license': manifest.get('license'),
        'depends': manifest.get('depends', []),
        'manifest': str(path),
    }
major = str(release.version).split('.')[0]
all_found = all(modules[name]['found'] for name in REQUIRED + BRIDGES)
report = {
    'version': release.version,
    'expected_major_version': '19',
    'version_matches': major == '19',
    'standard_source_modules': modules,
    'all_standard_sources_found': all_found,
    'note': 'Pemeriksaan file sumber. Status instalasi dalam database harus diperiksa terpisah.',
}
print(json.dumps(report, ensure_ascii=False, indent=2))
sys.exit(0 if major == '19' and all_found else 1)
