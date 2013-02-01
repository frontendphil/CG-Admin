from xhtml2pdf.pisa import CreatePDF
from jinja2 import BaseLoader, TemplateNotFound, Environment
from StringIO import StringIO
from os.path import exists, getmtime

from cgadmin.settings import PDF_TPL_PATH


class TemplateLoader(BaseLoader):

    def get_source(self, environment, template):
        path = "%s/%s" % (PDF_TPL_PATH, template)

        if not exists(path):
            raise TemplateNotFound(template)

        mtime = getmtime(path)

        with file(path) as f:
            source = f.read().decode("utf-8")

        return source, path, lambda: mtime == getmtime(path)


class PDFWriter(object):

    def __init__(self):
        self.env = Environment(loader=TemplateLoader())
        self.out = StringIO()

    def prepare_html(self, name, **kwargs):
        template = self.env.get_template(name)

        return template.render(**kwargs)

    def create_pdf(self, content):
        pdf = CreatePDF(src=content,
                        dest=self.out)

        if pdf.err:
            return None

        return self.out.getvalue()

    def pdf_for_patient(self, patient):
        html = self.prepare_html("patient.tpl", patient=patient,
                                                insurance=patient.get_insurance(),
                                                prescriptions=patient.get_prescriptions())

        return self.create_pdf(html)

    def pdf_for_prescription(self, patient, prescription, official):
        html = self.prepare_html("prescription.tpl", prescription=prescription,
                                                     patient=patient,
                                                     official=official)

        return self.create_pdf(html)
