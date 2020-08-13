#!/usr/bin/env python
import sys
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter
import os

# main
def main(file_name):
    laparams = LAParams()
    pagenos = set()
    maxpages = 0
    password = b''
    rotation = 0
    caching=0
    dir=os.getcwd()
    fname=dir+"/{}.pdf".format(file_name)
    with open(fname, 'rb') as fp:
        rsrcmgr = PDFResourceManager(caching=caching)
        outfp = open(dir+"/{}.md".format(file_name), 'w', encoding="utf-8")
        device = TextConverter(rsrcmgr, outfp, laparams=laparams,
                               imagewriter=None)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, pagenos,
                                      maxpages=maxpages, password=password,
                                      caching=caching, check_extractable=True):
            page.rotate = (page.rotate+rotation) % 360
            interpreter.process_page(page)
    device.close()
    outfp.close()
    return

if __name__ == '__main__':
    for fl in os.listdir(os.getcwd()):
        if fl.endswith(".pdf"):
            main(fl.replace(".pdf",""))
