import os
import hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader,TextLoader


# 获取文件的md5十六进制字符串
def get_file_md5_hex(file_path:str) -> str:
    if not os.path.exists(file_path):
        logger.error(f"[md5计算]文件{file_path}不存在！")
        return

    if not os.path.isfile(file_path):
        logger.error(f"[md5计算]路径{file_path}不是文件！")
        return

    md5_obj = hashlib.md5()

    chunk_size = 4096  # 以4kb分片

    try:
        with open(file_path, "rb") as f:   # 必须二进制读取
            while chunk := f.read(chunk_size): md5_obj.update(chunk)
            md5_hex = md5_obj.hexdigest()
            return md5_hex

    except Exception as e:
        logger.error(f"计算文件{file_path}md5值失败，{str(e)}")
        return None


# 返回文件夹的文件列表（运训的文件类型后缀）
def listdir_with_allowed_type(path:str,allowed_types:tuple[str]) -> list:
    files = []

    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]{path}不是文件夹！")
        return allowed_types

    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))

    return tuple(files)

# PDF文档加载
def pdf_loader(file_path:str,passwd = None) -> list[Document]:
    return PyPDFLoader(file_path,passwd).load()

# TXT文档加载
def txt_loader(file_path:str) -> list[Document]:
    return TextLoader(file_path,encoding="utf-8").load()
