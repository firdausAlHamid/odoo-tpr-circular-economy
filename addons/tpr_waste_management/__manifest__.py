# -*- coding: utf-8 -*-
{
    'name': 'TPR Waste Management',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/Waste Management',
    'summary': 'Pencatatan sisa potongan pelat (remnant), karantina, inspeksi kelayakan, dan penelusuran sisa CV Teknika Prima Raya',
    'description': """
TPR Waste Management
====================
Modul pengelolaan sisa potongan material pelat CV Teknika Prima Raya:
- Pencatatan nomor identitas unik sisa potongan (remnant/scrap)
- Metadata geometris potongan dalam milimeter (mm) dan massa riil dalam kilogram (kg)
- Alur karantina dan inspeksi kelayakan oleh petugas pemeriksa berwenang
- Penetapan status Reusable Remnant vs Scrap Fisik
- Penelusuran asal Manufacturing Order (MO), Proyek, dan transaksi stok fisik
- Relokasi stok standar tanpa manipulasi saldo stock.quant langsung
    """,
    'author': 'CV Teknika Prima Raya / Daus',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'product',
        'stock',
        'mrp',
        'project',
        'tpr_circular_core',
    ],
    'data': [
        'security/tpr_waste_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/tpr_waste_demo_data.xml',
        'views/tpr_remnant_cut_views.xml',
        'views/mrp_production_views.xml',
        'views/tpr_mfa_analysis_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
