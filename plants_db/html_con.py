import docx2txt
import PyPDF2
from tqdm import tqdm

import os
import requests
from urllib import urlopen, urlretrieve
from lxml import etree
import xml.etree.ElementTree as ET
import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urlparse import urlparse, urljoin

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_images(url, img_names):
    """
    Returns all image URLs on a single `url`
    """
    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
            # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        # finally, if the url is valid
        if is_valid(img_url):
            for img_name in img_names:
                if img_name in img_url:
                    urls.append(img_url)
    return urls

def download(url, pathname,rename_doc=""):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    print(pathname)
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    if rename_doc != "":
        filename = os.path.join(pathname, rename_doc)
    else:
        filename = os.path.join(pathname, url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), "Downloading {filename}".format(filename=filename), total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb+") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))
    return filename


def docx_to_text(docx_file, text_file=None):
    # replace following line with location of your .docx file
    if text_file is None:
        text_file = docx_file.replace("docx","txt")
    if text_file == 1:
        text_file = docx_file.replace(".docx","_1.txt")
    print(docx_file, text_file)
    MY_TEXT = docx2txt.process(docx_file)
    text_fobj = open(text_file, "w+")
    text_fobj.write(MY_TEXT.encode('utf-8'))
    text_fobj.close()

def pdf_to_text(pdf_file, text_file=None):
    if text_file is None:
        text_file = pdf_file.replace("pdf","txt")
    if text_file == 1:
        text_file = docx_file.replace(".docx","_1.txt")
    print(docx_file, text_file)
    MY_TEXT = docx2txt.process(docx_file)
    text_fobj = open(text_file, "w+")
    text_fobj.write(MY_TEXT.encode('utf-8'))
    text_fobj.close()

def pdf_to_text(pdf_file, text_file=None):
    if text_file is None:
        text_file = pdf_file.replace("pdf","txt")
    if text_file == 1:
        text_file = pdf_file.replace(".pdf","_1.txt")
    print(pdf_file, text_file)
    pdfFileObject = open(pdf_file, 'rb')
    text_file_obj = open(text_file,'w+')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)

    print(" No. Of Pages :", pdfReader.numPages)

    for page in range(pdfReader.numPages):
        pageObject = pdfReader.getPage(page)
        
        txt = pageObject.extractText()
        text_file_obj.write(txt.encode('utf-8'))
    text_file_obj.close()
    pdfFileObject.close()


def text_to_text(text_file_in, text_file_out):
    fin = open(text_file_in,"r")
def text_to_text(text_file_in, text_file_out):
    fout = open(trxt_file_out,"w")
    fout.write(fin.read())

#test downlaod iamge from web ^^


def extract_table_definition_usda(html):
    
