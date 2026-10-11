# -*- coding: utf-8 -*-
{
    'name': 'TPR Circular Core',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/Material',
    'summary': 'Master data material bersama untuk sirkularitas manufaktur CV Teknika Prima Raya',
    'description': """
TPR Circular Core
=================
Modul inti bersama untuk mendukung sirkularitas manufaktur dan waste management:
- Master data keluarga material (Carbon Steel, Stainless, Aluminium, dll)
- Master data grade material (SS400, ASTM A36, SUS304, dll)
- Master data ketebalan nominal pelat (mm)
- Ekstensi metadata dimensi (mm) dan massa (kg) pada katalog produk/material pelat
    """,
    'author': 'CV Teknika Prima Raya / Daus',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'product',
        'stock',
    ],
    'data': [
        'security/tpr_circular_core_security.xml',
        'security/ir.model.access.csv',
        'data/tpr_material_data.xml',
        'views/tpr_material_views.xml',
        'views/product_template_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
