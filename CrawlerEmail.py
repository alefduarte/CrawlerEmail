# -*- conding: utf8 
try:
    from urllib.parse import urlsplit
except ImportError:
     from urlparse import urlparse

from sys import platform
from collections import deque
import re
import csv
import os
import requests
import requests.exceptions
from bs4 import BeautifulSoup

urls_usadas = set()
emails = []
b = open('backup_emails.txt', 'w')

def get_links(URL, escolha):
    doc_html = deque([URL])

    while len(doc_html):
        url = doc_html.popleft()
        urls_usadas.add(url)
        try:
            partes = urlsplit(url)
        except:
            partes = urlparse(url)
        base_url = "{0.scheme}://{0.netloc}".format(partes)
        caminho = url[:url.rfind('/')+1] if '/' in partes.path else url
        ext = [".gif", ".jpg", ".jpeg", ".png", ".bmp"]
       
        if escolha == '2':
            print("\nAnalisando {} \nuse ctrl+c para parar".format(url))
            try:
                response = requests.get(url)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                continue
            email = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", 
            response.text, re.I))
            if email:
                print("Capturado:")
                for line in email:
                    b.write(line + "\n")
                    b.flush()
                    print(line)
                    if line not in emails:
                        emails.append(line)
            if platform == "linux" or platform == "linux2":
                soup = BeautifulSoup(response.text, "lxml")
            elif platform == "win32":
                soup = BeautifulSoup(response.text, "html.parser")
            for anchor in soup.find_all("a"):
                link = anchor.attrs["href"] if "href" in anchor.attrs else ''
                if link.startswith('/') and not link.endswith(tuple(ext)):
                    link = base_url + link
                elif not link.startswith('http') and not link.startswith('https') \
                and not link.endswith(tuple(ext)):
                    link = caminho + link
                if not link in doc_html and not link in urls_usadas:
                    doc_html.append(link)
        else:
            if url.startswith(URL.split('.com')[0]):
                print("\nAnalisando {} \nuse ctrl+c para parar".format(url))
                try:
                    response = requests.get(url)
                except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                    continue
                email = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", 
                response.text, re.I))
                if email:
                    print("Capturado:")
                    for line in email:
                        b.write(line + "\n")
                        b.flush()
                        print(line)
                        if line not in emails:
                            emails.append(line)
                if platform == "linux" or platform == "linux2":
                    soup = BeautifulSoup(response.text, "lxml")
                elif platform == "win32":
                    soup = BeautifulSoup(response.text, "html.parser")
                for anchor in soup.find_all("a"):
                    link = anchor.attrs["href"] if "href" in anchor.attrs else ''
                    if link.startswith('/') and not link.endswith(tuple(ext)):
                        link = base_url + link
                    elif not link.startswith('http') and not link.startswith('https') \
                    and not link.endswith(tuple(ext)):
                        link = caminho + link
                    if not link in doc_html and not link in urls_usadas:
                        doc_html.append(link)
                        
def salvarEmails():
    f = open('emails.txt', 'w')
    for line in emails:
        f.write("%s\n" % line)
    f.close()
    os.remove("backup_emails.txt")

def salvarEmailsCSV():
    cw = csv.writer(open("emails.csv",'w'))
    for line in emails:
        cw.writerow([line])


if __name__ == '__main__':
    try:
        input = raw_input
    except NameError:
        print(NameError.message)
    URL = input(u"Digite o link no formato http://algumacoisa.com\n")
    if not URL.startswith("http") or not URL.startswith("https"):
        URL = "https://" + URL
    try:
        link = "{0.scheme}://{0.netloc}/".format(urlsplit(URL))
    except:
        link = "{0.scheme}://{0.netloc}/".format(urlparse(URL))
    escolha = input("Escolha o metodo:\n 1 - Apenas os links iniciados com {}"
                    "\n 2 - Todos os links relacionados ao link (pode entrar"
                    "em varios sites)\n".format(link))
    try:
        get_links(URL, escolha)
        b.close()
        salvarEmails()
        salvarEmailsCSV()
    except KeyboardInterrupt:
        b.close()
        salvarEmails()
        salvarEmailsCSV()
