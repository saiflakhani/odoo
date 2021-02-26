{
    'name': "Rishabh Resume",
    'summary': "Rishabh Resume",
    'description': """Rishabh Resume Parser""",
    'author': "Alka Harbalkar",
    'license': "AGPL-3",
    'website': "http://www.resumeparser.com",
    'category': 'Uncategorized',
    'version': '11.0.1.0.0',
    'depends': ['base', 'website', 'hr_recruitment', 'website_form', 'website_mail', 'web', 'website_hr_recruitment'],
    'data': [
            'security/ir.model.access.csv'
            , 'views/resume_view.xml'
            ],
    'sequence': 2,
    'installable': True,
    "external_dependencies": {
         'python37': ['numpy', 'pyresparser', 'pandas']
     },

}