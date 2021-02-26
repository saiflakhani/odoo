# -*- coding: utf-8 -*-

import os
import io
from jsonschema import ValidationError
from odoo import fields, models, api
from odoo.modules.module import get_resource_path
import logging
#from pyresparser import ResumeParser
import base64
# import StringIO
from . import utils
from .resume_parser import ResumeParser


_logger = logging.getLogger(__name__)


class Resume(models.Model):
    _description = 'Resume Parser'
    _inherit = 'hr.applicant'
    # _inherits = {'hr.applicant': "partner_name"}

    resume = fields.Binary()
    skills = fields.Text()
    college = fields.Char()
    experience = fields.Char()
    designation = fields.Char()
    company = fields.Char()
    education = fields.Char()
    address = fields.Char()
    location = fields.Char()
    file_name = fields.Char("File Name")
    resume1 = fields.Binary(compute='_get_applicant_resume', store=False, string='Applicant Resume')
    filename = fields.Char("File Name", store=False)

    @api.depends('partner_name')
    def _get_applicant_resume(self):
        for rec in self:
            record = self.env['ir.attachment'].sudo().search([('res_id','=',rec.id),
                                                              ('res_model','=','hr.applicant'),
                                                              ('res_name','=', rec.partner_name)
                                                              ], limit=1)
            if record:
                rec.resume1 = record.datas
                rec.filename = record.name
            else:
                rec.resume = False

    def parse_resume(self):
        try:
            resume_data = {}
            path = get_resource_path('resume', 'data')

            if self.resume:
                resume, filename = self.resume, self.file_name
            else:
                resume, filename = self.resume1, self.filename

            file_path = path + '/' + filename
            with open(file_path, 'wb') as f:
                f.write(base64.b64decode(resume))
            if not isinstance(file_path, io.BytesIO):
                ext = os.path.splitext(file_path)[1].split('.')[1]
            else:
                ext = file_path.name.split('.')[1]
            resume_text = utils.extract_text(file_path, '.'+ext)

            if self.resume:
                # resume_data['name'] = utils.extract_name(resume_text)
                resume_data['partner_name'] = utils.extract_name(resume_text)
                resume_data['partner_phone'] = utils.extract_mobile_number(resume_text)
                resume_data['email_from'] = utils.extract_email(resume_text)
            else:
                if self.partner_name is None or self.partner_name == '':
                    # resume_data['name'] = utils.extract_name(resume_text)
                    resume_data['partner_name'] = utils.extract_name(resume_text)
                if self.partner_phone is None or self.partner_phone == '':
                    resume_data['partner_phone'] = utils.extract_mobile_number(resume_text)
                if self.email_from is None or self.email_from == '':
                    resume_data['email_from'] = utils.extract_email(resume_text)

            resume_data['skills'] = ','.join(utils.extract_skills(resume_text)).strip()
            # if utils.extract_education(resume_text):
            #     if len(utils.extract_education(resume_text)) > 0:
            #         resume_data['education'] = utils.extract_education(resume_text)

            entities = utils.extract_entities_wih_custom_model(resume_text)
            if entities:
                for k, v in entities.items():
                    if k == 'Address':
                        resume_data['address'] = ''.join(entities['Address'])
                    if k == 'Years of Experience':
                        resume_data['experience'] = ''.join(entities['Years of Experience'])
                    if k == 'Designation':
                        resume_data['designation'] = ','.join(entities['Designation'])

                    if k == 'College Name':
                        resume_data['college'] = ','.join(entities['College Name'])
                    if k == 'Companies worked at':
                        resume_data['company'] = ','.join(v).strip()
                    if k == 'Location':
                        resume_data['location'] = ','.join(entities['Location'])
            self.write(resume_data)
            path_remove = os.path.join(file_path)
            os.remove(path_remove)
        except TypeError as e:
            raise ValidationError(u'ERROR: {}'.format(e))

