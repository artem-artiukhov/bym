"""PDF generator module."""

from io import BytesIO

from flask import render_template
from weasyprint import HTML


class Filetypes:

    PNG = '.png'
    PDF = '.pdf'


class BasePDFGenerator:
    template_name = None

    def __new__(cls, *args, **kwargs):
        if cls is BasePDFGenerator:
            raise TypeError(f'{cls.__name__} class cannot be directly instantiated')
        return super().__new__(cls)

    def generate_pdf(self, *args, **kwargs):
        """Convert rendered content to WeasyPrint HTML structure."""
        cnt = self._render_content()
        return HTML(string=cnt, *args, **kwargs)

    def generate_pdf_file(self, *args, **kwargs):
        """Generate file-like pdf object for easier upload."""
        pdf_in_mem = BytesIO()
        self.generate_pdf(*args, **kwargs).write_pdf(pdf_in_mem)
        pdf_in_mem.name = self._generate_name()
        pdf_in_mem.seek(0)
        return pdf_in_mem

    def generate_png_file(self, *args, **kwargs):
        """Generate file-like png object for easier upload."""
        png_in_mem = BytesIO()
        self.generate_pdf(*args, **kwargs).write_png(png_in_mem)
        png_in_mem.name = self._generate_name(ftype=Filetypes.PNG)
        png_in_mem.seek(0)
        return png_in_mem

    def _render_content(self):
        """Render content based on context."""
        ctx = self._get_rendering_context()
        return render_template(self.template_name, **ctx)

    def _get_rendering_context(self):
        """Get context information for rendering a template."""
        return {}

    def _generate_name(self, ftype=Filetypes.PDF):
        """Generate filename."""
        pass


class ArticlePDFGenerator(BasePDFGenerator):
    template_name = 'pdf/article.html'

    def __init__(self, dumped_article):
        """Constructor."""
        self._article = dumped_article

    def _get_rendering_context(self):
        """Get context information for rendering a template."""
        # No any additional processing
        return self._article

    def _generate_name(self, ftype=Filetypes.PDF):
        """Generate filename based on title."""
        return f'{self._article.get("title", "UNKNOWN_ARTICLE_TITLE")}{ftype}'
