import sys
import requests
import simplejson
from typing import Optional
from book import Book, Page, Content, ContentType, TableContent
from model import Model
from translator.pdf_parser import PDFParser
from translator.writer import Writer
from translator.prompt_maker import PromptMaker
from utils import LOG

class PDFTranslator:
    def __init__(self, model: Model):
        self.model = model
        self.pdf_parser = PDFParser()
        self.writer = Writer()
        self.prompt_maker = PromptMaker()

    def translate_pdf(self, pdf_file_path: str, file_format: str = 'PDF', target_language: str = '中文', output_file_path: str = None, pages: Optional[int] = None):
        self.book = self.pdf_parser.parse_pdf(pdf_file_path, pages)

        for page_idx, page in enumerate(self.book.pages):
            for content_idx, content in enumerate(page.contents):
                prompt = self.prompt_maker.translate_prompt(content, target_language)
                LOG.info(f"[prompt]{prompt}")
                translation, status = self.model.make_request(prompt)
                LOG.info(f"[translation]{translation}")
                
                # Update the content in self.book.pages directly
                self.book.pages[page_idx].contents[content_idx].set_translation(translation, status)

        self.writer.save_translated_book(self.book, output_file_path, file_format)


    def _translate(self, payload):
        try:
            response = requests.post(self.model.model_url, json=payload, timeout=self.model.timeout)
            response.raise_for_status()
            response_dict = response.json()
            translation = response_dict["response"]
            return translation, True
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求异常：{e}")
        except requests.exceptions.Timeout as e:
            raise Exception(f"请求超时：{e}")
        except simplejson.errors.JSONDecodeError as e:
            raise Exception("Error: response is not valid JSON format.")
        except Exception as e:
            raise Exception(f"发生了未知错误：{e}")
        return "", False
