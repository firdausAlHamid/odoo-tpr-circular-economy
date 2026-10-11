"""Prepare local configuration without replacing existing credentials."""
from pathlib import Path
import secrets


def setup(project_root):
    project_root = Path(project_root)
    env_path = project_root / '.env'
    conf_path = project_root / 'config' / 'odoo.conf'
    if env_path.exists() and conf_path.exists():
        print('Konfigurasi sudah ada. Tidak ada file yang diganti.')
        return
    if env_path.exists() or conf_path.exists():
        raise SystemExit(
            'Konfigurasi baru tersedia sebagian. Periksa .env dan config/odoo.conf. '
            'Setup berhenti tanpa mengganti file yang ada.'
        )
    env_template = (project_root / '.env.example').read_text(encoding='utf-8')
    conf_template = (project_root / 'config' / 'odoo.conf.example').read_text(encoding='utf-8')
    if 'CHANGE_ME_DATABASE_PASSWORD' not in env_template:
        raise SystemExit('Template .env tidak memiliki penanda password yang diperlukan.')
    if 'CHANGE_ME_MASTER_PASSWORD' not in conf_template:
        raise SystemExit('Template Odoo tidak memiliki penanda master password yang diperlukan.')
    env_text = env_template.replace('CHANGE_ME_DATABASE_PASSWORD', secrets.token_hex(24))
    conf_text = conf_template.replace('CHANGE_ME_MASTER_PASSWORD', secrets.token_hex(24))
    with env_path.open('x', encoding='utf-8', newline='\n') as file:
        file.write(env_text)
    with conf_path.open('x', encoding='utf-8', newline='\n') as file:
        file.write(conf_text)
    print('Siap. .env dan config/odoo.conf dibuat dengan password lokal baru.')
    print('Master password untuk membuat database ada pada admin_passwd di config/odoo.conf.')
    print('Berikutnya jalankan: docker compose up -d')


if __name__ == '__main__':
    setup(Path(__file__).resolve().parent.parent)
