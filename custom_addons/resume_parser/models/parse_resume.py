import base64
from io import BytesIO

from .pyresparser.pyresparser import ResumeParser
import simplejson as json
from odoo import models, fields

## TODO get this data from XPATH
# data = ResumeParser('/Users/saif/Pictures/Gaurav_Resume.pdf').get_extracted_data()

class ApplicantApplicant(models.Model):
    _name = "applicant.applicant"
    name = fields.Char(string="Name")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
    email = fields.Char(string="Email")
    mobile_number = fields.Char(string="Mobile Number")
    skills = fields.Char(string="Skills")
    college_names = fields.Char(string="College Names")
    resume_file = fields.Binary(string="Upload Resume")
    resume_file_name = fields.Char(string="Filename")
    degree = fields.Text(string="Degree")
    experience = fields.Text(string="Experience")
    exp_years = fields.Float(string="Years of Experience")
    company_names = fields.Char(string="Company Names")


    def import_resume_data(self):
        # file_content = base64.decodebytes(self.resume_file)
        # inputx = BytesIO()
        # inputx.write(file_content)
        # inputx.name = str(self.resume_file_name.split("."))[1]
        print("File name is ---> ", str(self.resume_file_name))
        print("." + str(self.resume_file_name.strip().split(".")[1]))

        bytes = base64.b64decode(self.resume_file, validate=True)
        bytesio = BytesIO(bytes)
        bytesio.name = "." + str(self.resume_file_name.strip().split(".")[1])
        # parsed_data = ResumeParser(bytesio).get_extracted_data()



        # f = open(self.resume_file_name, "w")
        # f.write(str(file_content))
        # f.close()

        data = ResumeParser(bytesio).get_extracted_data()
        print(data)
        self.name = data['name']
        self.email = data['email']
        self.mobile_number = data['mobile_number']
        if data['skills'] is not None:
            self.skills = str(', '.join(data['skills']))
        if data['college_name'] is not None:
            self.college_names = str(', '.join(data['college_name']))
        self.degree = str(data['degree'])
        if data['experience'] is not None:
            self.experience = str(', '.join(data['experience']))
        self.exp_years = data['total_experience']
        if data['company_names'] is not None:
            self.company_names = str(', '.join(data['company_names']))






## This class was created before, and will not be used anymore
## Preserving for DB reasons
class StudentStudent(models.Model):
    _name = "student.student"
    name = fields.Char(string="Name")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
    email = fields.Char(string="Email")
    mobile_number = fields.Char(string="Mobile Number")
    skills = fields.Text(string="Skills")
    resume_file = fields.Binary(string="Upload Resume")


