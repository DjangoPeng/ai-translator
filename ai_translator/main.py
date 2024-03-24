import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel
from translator import PDFTranslator
from argparse import ArgumentParser

if __name__ == "__main__":
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--config",  help="Path to configuration file" ,default="/Users/linyan/Documents/worksp/openai-translator/config.yaml")
    argument_parser.add_argument("--model_type", help="Type of model (e.g., OpenAIModel, GLMModel)",default="OpenAIModel")
    argument_parser.add_argument("--openai_model", help="Name of OpenAI model")
    argument_parser.add_argument("--openai_api_key", help="OpenAI API key")
    argument_parser.add_argument("--timeout", help="Timeout for GLMModel")
    argument_parser.add_argument("--model_url", help="URL for GLMModel")
    argument_parser.add_argument("--book", help="Path to book file")  # 添加 --book 参数
    argument_parser.add_argument("--file_format", help="File format")  # 添加 --file_format 参数
    args = argument_parser.parse_args()
    config_loader = ConfigLoader(args.config)
    print("Config path:", config_loader)
    config = config_loader.load_config()
    if hasattr(args, "model_type"):
        if args.model_type == "OpenAIModel":
            model_name = args.openai_model if args.openai_model else config['OpenAIModel']['model']
            api_key = args.openai_api_key if args.openai_api_key else config['OpenAIModel']['api_key']
            model = OpenAIModel(model=model_name, api_key=api_key)
        elif args.model_type == "GLMModel":
            timeout = args.timeout if args.timeout else config['GLMModel']['timeout']
            model_url = args.model_url if args.model_url else config['GLMModel']['model_url']
            model = GLMModel(model_url=model_url, timeout=timeout)
        else:
            raise ValueError("Invalid model_type specified. Please choose either 'GLMModel' or 'OpenAIModel'.")
    else:
        raise ValueError("Model type not provided. Please provide a model_type argument.")

    pdf_file_path = args.book if args.book else config['common']['book']
    file_format = args.file_format if args.file_format else config['common']['file_format']

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    translator.translate_pdf(pdf_file_path, file_format)
