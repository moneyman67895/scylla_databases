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
    fout = open(trxt_file_out,"w")
    fout.write(fin.read())

#test downlaod iamge from web ^^

# get html from site and write to local file
plantImagePage = "https://plants.sc.egov.usda.gov{0}"
plantHeaderPage = "https://plants.sc.egov.usda.gov/core/profile?symbol={0}"
plantCharacteristicsPage= "https://plants.sc.egov.usda.gov/java/charProfile?symbol={0}"

allPlants = "https://plants.sc.egov.usda.gov/java/characteristics"
headers = {'Content-Type': 'text/html',}
headers = {'Content-Type': 'text/html',}
response = requests.get(allPlants)
html = response.text


home_dir = "/home/james/git_repos/scylla_databases/plants_db"


with open (home_dir + '/usda/plants_usda.html', 'wb+') as f, open (home_dir + '/usda/plants_usda.xml', 'wb+') as f1:
    f.write(html.encode("utf-8"))
    f1.write(html.encode("utf-8"))
    
# read local html file and set up lxml html parser
local = home_dir + '/usda/plants_usda.html'
response = urlopen(local)
htmlparser = etree.HTMLParser()
tree = etree.parse(response, htmlparser)

path1 =  tree.xpath("//body/table/tr[5]/td/table/tr/td[4]/table/tr[3]/td[1]/table/*")
print(path1)
plants_dict = {}
for element in path1[1:]:
    print(element)
    th1 = element.findall("th")[0]
    tds= element.findall("td")
    print(tds)#.items())
    a1 = tds[0].findall("a")
    if a1 == []:
        continue
    else: 
        a1 = a1[0]
    href= a1.get("href")
    symbol = href.split("=")[1]
    common_name = tds[1].text
    print(href, symbol)
    print(common_name)
    plants_dict[symbol] = {"main_page" : href, "Common_Name" : common_name, "General_Info" : {}, "Plant Fact Sheet in Adobe PDF format." : "", 'Plant Fact Sheet in Microsoft Word format.' : "", "Plant Guide in Adobe PDF format." : "", 'Plant Guide in Microsoft Word format.' : "", "characteristics" : {}, "characteristics_dict" : {}, "Classification" : {"Kingdom": "", "Subkingdom" : "", "Superdivision" : "", "Division" : "", "Class" : "", "Subclass": "", "Order" : "", "Family" : "" , "Genus" : "", "Species" : ""}, "USES" : {"Class Of Animal " : { "High" : [], "Low" : [], "Minor" : [], "Moderate" : []}, "Food_Percent_Of_Diet" : { "High" : 0, "Low" : 0, "Minor" : 0, "Moderate" : 0}, "Cover" : { "High" : None, "Low" : None, "Minor" : None, "Moderate" : None}}}


plants_dict_items = plants_dict.items()

all_plants_http_dir = home_dir + "/usda/plant_http"
count = 0
for (symbol, link) in plants_dict_items:

    print(symbol, link)
    plant_http_dir = all_plants_http_dir + "/{0}".format(symbol)
    plant_http_images_dir = plant_http_dir + "/images"
    plant_http_docs_dir = plant_http_dir + "/docs"
    os.chdir(all_plants_http_dir)
    print(os.listdir(all_plants_http_dir))

    if symbol not in os.listdir(all_plants_http_dir):
        os.mkdir(plant_http_dir)
        os.mkdir(plant_http_images_dir)
        os.mkdir(plant_http_docs_dir)

    html_header = plantHeaderPage.format(symbol)
    response_header = requests.get(html_header)
    header_text = response_header.text
    local_header = plant_http_dir + "/plant_{0}.html".format(symbol)
    with  open (local_header, 'wb+') as f1:
        f1.write(header_text.encode("utf-8"))


    html_characacteristics = plantCharacteristicsPage.format(symbol)
    response_characacteristics = requests.get(html_characacteristics)
    characteristics_text = response_characacteristics .text
    local_characteristics = plant_http_dir + "/plant_{0}_characteristics.html".format(symbol)
    with  open (local_characteristics , 'wb+') as f2:
        f2.write(characteristics_text.encode("utf-8"))

    response_header = urlopen(local_header)

    htmlparser_header = etree.HTMLParser()
    tree_header = etree.parse(response_header,htmlparser_header)

    tabs_that_exist = tree_header.xpath("/html/body/table/tr[5]/td/table/tr/td[4]/ul/li/a")
    parseable_sections = []
    for a in tabs_that_exist:
        print(a.text)
        parseable_sections.append(a.text.replace(" ","_"))
    print(tabs_that_exist)
    print(parseable_sections)

    if "Classification" in parseable_sections:

        print("")
        #plant classificatio nscientiffic, ~~ family, order, genus, species

        path2_classification = tree_header.xpath("/html/body/table/tr[5]/td/table/tr/td[4]/div[2]/div[4]/table/tr")
        print(path2_classification)
        for tr in path2_classification:
            tds = tr.findall("td")
            td_col = tds[0]
            td_val = tds[1]

            col = td_col.text
            a_val = td_val.findall('a')[0]
            val = a_val.text.replace("\n","").replace("\t","")
            if val == "":
                val = " ".join([em.text for em in a_val.findall('em')])
            print(col,val)
            plants_dict[symbol]["Classification"][col] = val
        print(plants_dict[symbol]["Classification"])

    if "General" in parseable_sections:
        #General

        path2_pdf = tree_header.xpath("//body/table/tr[5]/td/table/tr/td[4]/div[2]/div[1]/div[1]/table[2]/tr[9]/td/div/div")
        if path2_pdf == []:
           print("No pdf")
        else:
            print(path2_pdf)
            keys_map = {"key1" : {"Facts" : ("Fact Sheet" , "Facts", "info", "INFO"), "Guide" : ("Plant Guide")}, "key2" : [("pdf", pdf_to_text, "PDF","pdf") , ("docx",docx_to_text,"DOCX","docx","word", "Word"),("txt", text_to_text,"TXT","txt")]}
            for div in path2_pdf:

                strong = div.findall("strong")[0]
                strong_str = strong.text
                keys1 = keys_map["key1"]
                key1_to_use = ()
                
                for (key1,vals) in keys1.items():
                    if strong_str in vals:
                        key1_to_use = key1
                if key1_to_use == ():
                    continue
                elif key1_to_use not in plants_dict[symbol].keys():
                    plants_dict[symbol][key1_to_use] = {}

                a_htmls = div.findall("a")
                while a_htmls != []:
                    a = a_htmls.pop()
                    link = urljoin(html_header,a.get("href"))#.replace("..","")
                    downloaded = False
                    for key2 in keys_map["key2"]:
                        doc_type = key2[0]
                        conv_fn = key2[1]
                        keys2 = key2[2:]
                        for key2_ in keys2:
                            if key2_ in a.get("title"):
                                document =symbol + "_" + key1_to_use + "." + doc_type

                                download_doc = download(link,plant_http_docs_dir, document)
                                print("Downloaded from {0} to {1}, FILE TYPE \n\t\t{2} ~ for ~ {3}".format(link, document, doc_type,symbol))
                                if len(plants_dict[symbol][key1_to_use]) > 0:
                                    download_doc_text = conv_fn(download_doc,1)
                                else:
                                    download_doc_text = conv_fn(download_doc)
                                plants_dict[symbol][key1_to_use][doc_type] = {"link" : link, "local_dir" : download_doc, "local_dir_text" : download_doc_text}
                                downloaded = True
                                break
                        if downloaded is True:
                            break

        general_info = tree_header.xpath("//body/table/tr[5]/td/table/tr/td[4]/div[2]/div[1]/div[1]/table[2]/tr")
        #table_general_info = general_info[0].findall("tr")
        print(general_info)
        locations_docs = {}

        for tr in general_info:#table_general_info:
            print(tr)
            tds = tr.findall("td")
            if tds == []:
                continue
                print(tr.findall("div"))
            print(tds)
            general_info_column = tds[0].text
            print("TD text",general_info_column)
            if general_info_column  == ":" :
                subelements = tds[0].findall("a")
                if subelements == []:
                    continue
                a1 = subelements[0]
                strong = a1.findall("strong")
                if strong != []:
                    general_info_column = strong.text.strip()

            if general_info_column is None:
                td_a_0 = tds[0].findall('a')
                print("TD text", td_a_0)
                if td_a_0 == []:
                    general_info_column = tds[0].findall("strong")[0].text.strip()
                else:
                    print("A")
                    general_info_column  = td_a_0[0].text
                    if general_info_column is None:
                        general_info_column = td_a_0[0].findall('strong')[0].text
                    print(general_info_column)

            else:
                general_info_column = general_info_column.strip()
            general_info_column = general_info_column.replace("\n","").replace("\t","").strip(":")
            print("GIC1", general_info_column) 
            if len(tds) > 1:
                general_info_value = tds[1].text.strip()
            else:
                if general_info_column in ('Plant Guide', 'Fact Sheet'):
                    locations_docs[general_info_column] = i
                continue
            print(locations_docs)

            plants_dict[symbol]["General_Info"][general_info_column] = general_info_value
            
        for key in plants_dict[symbol]["General_Info"]:
            print(key)


        # if general section then should be a characteristic section
        response_characteristics = urlopen(local_characteristics)
        htmlparser_characteristics = etree.HTMLParser()
        tree_characteristics = etree.parse(response_characteristics, htmlparser_characteristics)
        path2_characteristics = tree_characteristics.xpath("//body/table/tr[5]/td/table/tr/td[4]/table/tr[3]/td[1]/table")

        subsection = ""
        
        tr = path2_characteristics[0].findall("tr")[0]
        td = tr.findall("td")[0]
        subsection = td.text
        plants_dict[symbol]["characteristics"][subsection] = []
        plants_dict[symbol]["characteristics_dict"][subsection] = {}
        trs = path2_characteristics[0].findall("tr")[1:]

        for tr in trs:
            tds = tr.findall("td")
            if tds != []:
                if len(tds) == 1:
                    subsection = tds[0].text
                    plants_dict[symbol]["characteristics"][subsection] = []
                    plants_dict[symbol]["characteristics_dict"][subsection] = {}
                    print("\n\n")
                    print(plants_dict[symbol]["characteristics_dict"].keys())
                    print("\n\n")
                else:

                    print(tds)

                    column_name = tds[0].text
                    column_value = tds[1].text
                    if column_name is not None:
                        print(column_name, column_value)
                        plants_dict[symbol]["characteristics"][subsection].append((column_name, column_value))
                        plants_dict[symbol]["characteristics_dict"][subsection][column_name] = column_value 
        if count > 5:
            break
        count += 1
        
    else:
        print("Error")
    if "Images" in parseable_sections:
        print("")

    '''
    #images for plant based on order ,genus, species
    path2_imgs = tree2.xpath("//body/table/tr[5]/td/table/tr/td[4]/div[2]/div[2]/div[2]/div/div/div[1]/a")

    for a in path2_imgs:#.findAll("div"):
        img_dir = "/home/james/plant_http/{0}/images/".format(symbol)#,a.get("href").split("/")[-1].split("=")[-1])
        url_img = plantImagePage.format(a.get("href"))
        resp = urlopen(url_img)
        htmlparser3 = etree.HTMLParser()
        tree3 = etree.parse(resp, htmlparser3)
        img_url = tree3.xpath("/html/body/table/tr[5]/td/table/tr/td[4]/table/tr[3]/td[1]/p[5]/img")[0].get("src")
        pathimg = "{0}{1}".format(url_img,img_url)
        print(pathimg)
        img_name = a.get("href").split("/")[-1].split("=")[-1]
        img_name = "_".join(img_name.split("_")[0:2])
        #imgs = get_all_images(url_img, [img_name])
        imgs = []
        for img in imgs:
            download(img,img_dir)
            print(img)
    '''


def infer_type(value):#returns the type of data
    try:
        val = int(value)
        return "int"

    except Exception as e:
        try:
        #nesting thos try excepts, needs anew arisot gun        
            val = float(value)
            return "float"
        except Exception as e:
            
            try:
                #default str for vale in this htmls database, but hwat about all htmls
                val = str(value)
                return "text"
            except Exception as e:
                return e

#create database from any source of information, may be temporary and passed to a larger set of database, according to some machine learning mapping based on name/values,....
#check_type_infereed, is a threshold for data from this source
#at the poit were the inferred type is obvious, that is most data (out of how many), do we know the start and head end ahead of time or is there an unkown, or perhaps time based stream of data, when is ifnerence not allowed...


#right now, its an html, has a limit
#yo gunna opay me

def get_index(type_ , types):
    for (i,t) in (range(len(types)), types):
        if t == type_:
            return i
    raise Exception("NotInTable")
    #-1 in python, and if array is an obejct.... wwat do we search by.. LIKE SCYHLLA... oh search by values of object by order of uniquity, seperate data based on uniquity, cluster by dimensions used for visualization? or dimensions object is becomes a data point by how objects of same value types, (inferring we're saying a value type is a attribute, we should still be able to infer type from unkown sources, using basic statistics)

    #TRUTH, where my pay check governemnt and God is real, I miss me. 1+ 1 = 2.

def fib(n=5):
    if n == 1:
        return  1
    else:
        return fib(n-1) + fib(n-2)


class create_column_table:
    def __init__(self, column, value):
        self.column = column
        self.types = {infer_type(value) : 1}

        self.type = None
    def add_value_type(self, inferred_type):

        if self.type is None:
            try:
                type_index = get_index(inferred_type, self.types)
                self.types[type_index] += 1
            except Exception as e:
                if str(e) == "NotInTable":
                    
                    #redundant unless exception is predeffinned according to pythons try except, would needd to know hwat kind of exception to use for the particulr custom program.. or just use an if
                    self.types[inferred_type] = 1

            self.type = self.check_type_inferred(5)

    def check_type_inferred(self, min_to_verify=5):
        for (k,v) in self.types.items():
            if v > 5:
                return k
        return None

d
    def get_type(self):
        if self.type is not None:
            return self.type

        max_count = 0
        type_column = self.types.items()[0][0]
        for (k,v) in self.types.items():
            if v > max_count:
                type_column = k
                max_count = v

        return type_column
    def get_column(self):
        column = self.column


ZZ


def plants_dict_to_data_base(plants_dict):

    plants_dict_characteristics = [(symbol, plant_dict) for (symbol, plant_dict) in plants_dict.items()]
    create_columns = []
    insert_values = []
           

    for (symbol, plant_dict) in plants_dict_characteristics:
        row_characteristics = USDA_From_HTML()
        for (subsection, characteristics) in plant_dict["characteristics"].items():
            i = 0
            print(subsection)
            for (characteristic_column, characteristic_value) in characteristics:
                characteristic_column= str(characteristic_column.encode('utf-8'))

                if characteristic_value is None:
                    characteristic_value = "NULL"

                characteristic_value = str(characteristic_value.encode('utf-8'))

                print(characteristic_column + " : "  + characteristic_value)
                i += 1
                row_characteristic.addValue(characteristic_column, characteristic_value)

                insert_values.append((characteristic_column,characteristic_value))

                if characteristic_column not in [c.column for c in create_columns]:
                    column_new = create_column_table(characteristic_column, characteristic_value)
                    create_columns.append(column_new)
                    print(" | ".join([c.column + " " + str(c.type) for c in create_columns]))
                else:
                    j = 0
                    while j < len(create_columns):
                        if create_columns[j].column == characteristic_column:
                            create_columns[j].add_value_type(infer_type(characteristic_value))
                            break
                        j +=  1

    create_table = "CREATE TABLE characteristic_table ( " + ",".join([c.get_column() + " " + c.get_type() for c in create_columns]) +")" 
    print(create_table)

    exit(1)



plants_dict_to_data_base(plants_dict)
