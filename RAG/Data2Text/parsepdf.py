# ��ȡPDF
import PyPDF2
# ����PDF��layout����ȡ�ı�
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
# ��PDF�ı������ȡ�ı�
import pdfplumber
# ��PDF����ȡͼƬ
from PIL import Image
from pdf2image import convert_from_path
# ����OCR��ͼƬ����ȡ�ı�
import pytesseract
# ��������еĸ��ֹ����ļ�
import os


# ����һ���ı���ȡ����

def text_extraction(element):
    # ����Ԫ������ȡ�ı�
    line_text = element.get_text()

    # ̽���ı��ĸ�ʽ
    # ���ı����г��ֵ����и�ʽ��ʼ���б�
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            # �����ı����е�ÿ���ַ�
            for character in text_line:
                if isinstance(character, LTChar):
                    # ׷���ַ���font-family
                    line_formats.append(character.fontname)
                    # ׷���ַ���font-size
                    line_formats.append(character.size)
    # �ҵ�����Ψһ�������С������
    format_per_line = list(set(line_formats))

    # ���ذ���ÿ���ı������ʽ��Ԫ��
    return (line_text, format_per_line)


# ����һ����pdf�вü�ͼ��Ԫ�صĺ���
def crop_image(element, pageObj):
    # ��ȡ��PDF�вü�ͼ�������
    [image_left, image_top, image_right, image_bottom] = [element.x0,element.y0,element.x1,element.y1]
    # ʹ������(left, bottom, right, top)�ü�ҳ��
    pageObj.mediabox.lower_left = (image_left, image_bottom)
    pageObj.mediabox.upper_right = (image_right, image_top)
    # ���ü����ҳ�汣��Ϊ�µ�PDF
    cropped_pdf_writer = PyPDF2.PdfWriter()
    cropped_pdf_writer.add_page(pageObj)
    # ���ü��õ�PDF���浽һ�����ļ�
    with open('cropped_image.pdf', 'wb') as cropped_pdf_file:
        cropped_pdf_writer.write(cropped_pdf_file)

# ����һ����PDF����ת��Ϊimage�ĺ���
def convert_to_images(input_file,):
    images = convert_from_path(input_file)
    image = images[0]
    output_file = "PDF_image.png"
    image.save(output_file, "PNG")

# ������ͼƬ����ȡ�ı��ĺ���
def image_to_text(image_path):
    # ��ȡͼƬ
    img = Image.open(image_path)
    # ��ͼƬ�г�ȡ�ı�
    text = pytesseract.image_to_string(img)
    return text

# ��ҳ������ȡ�������

def extract_table(pdf_path, page_num, table_num):
    # ��PDF�ļ�
    pdf = pdfplumber.open(pdf_path)
    # �����Ѽ���ҳ��
    table_page = pdf.pages[page_num]
    # ��ȡ�ʵ��ı��
    table = table_page.extract_tables()[table_num]
    return table

# �����ת��Ϊ�ʵ��ĸ�ʽ
def table_converter(table):
    table_string = ''
    # ��������ÿһ��
    for row_num in range(len(table)):
        row = table[row_num]
        # ��warp������ɾ����·��·��
        cleaned_row = [item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item in row]
        # �����ת��Ϊ�ַ�����ע��'|'��'\n'
        table_string+=('|'+'|'.join(cleaned_row)+'|'+'\n')
    # ɾ�����һ�����з�
    table_string = table_string[:-1]
    return table_string


# ����PDF·��
pdf_path = 'OFFER 3.pdf'

# ����һ��PDF�ļ�����
pdfFileObj = open(pdf_path, 'rb')
# ����һ��PDF�Ķ�������
pdfReaded = PyPDF2.PdfReader(pdfFileObj)

# �����ֵ��Դ�ÿ��ͼ������ȡ�ı�
text_per_page = {}
# ���Ǵ�PDF����ȡҳ��
for pagenum, page in enumerate(extract_pages(pdf_path)):

    # ��ʼ����ҳ������ȡ�ı�����ı���
    pageObj = pdfReaded.pages[pagenum]
    page_text = []
    line_format = []
    text_from_images = []
    text_from_tables = []
    page_content = []
    # ��ʼ�����������
    table_num = 0
    first_element = True
    table_extraction_flag = False
    # ��pdf�ļ�
    pdf = pdfplumber.open(pdf_path)
    # �����Ѽ���ҳ��
    page_tables = pdf.pages[pagenum]
    # �ҳ���ҳ�ϵı����Ŀ
    tables = page_tables.find_tables()

    # �ҵ����е�Ԫ��
    page_elements = [(element.y1, element) for element in page._objs]
    # ��ҳ���г��ֵ�����Ԫ�ؽ�������
    page_elements.sort(key=lambda a: a[0], reverse=True)

    # �������ҳ���Ԫ��
    for i, component in enumerate(page_elements):
        # ��ȡPDF��Ԫ�ض�����λ��
        pos = component[0]
        # ��ȡҳ�沼�ֵ�Ԫ��
        element = component[1]

        # ����Ԫ���Ƿ�Ϊ�ı�Ԫ��
        if isinstance(element, LTTextContainer):
            # ����ı��Ƿ�����ڱ���
            if table_extraction_flag == False:
                # ʹ�øú�����ȡÿ���ı�Ԫ�ص��ı��͸�ʽ
                (line_text, format_per_line) = text_extraction(element)
                # ��ÿ�е��ı�׷�ӵ�ҳ�ı�
                page_text.append(line_text)
                # ����ÿһ�а����ı��ĸ�ʽ
                line_format.append(format_per_line)
                page_content.append(line_text)
            else:
                # ʡ�Ա��г��ֵ��ı�
                pass

        # ���Ԫ���е�ͼ��
        if isinstance(element, LTFigure):
            # ��PDF�вü�ͼ��
            crop_image(element, pageObj)
            # ���ü����pdfת��Ϊͼ��
            convert_to_images('cropped_image.pdf')
            # ��ͼ������ȡ�ı�
            image_text = image_to_text('PDF_image.png')
            text_from_images.append(image_text)
            page_content.append(image_text)
            # ���ı��͸�ʽ�б������ռλ��
            page_text.append('image')
            line_format.append('image')

        # �����Ԫ��
        if isinstance(element, LTRect):
            # �����һ������Ԫ��
            if first_element == True and (table_num + 1) <= len(tables):
                # �ҵ����ı߽��
                lower_side = page.bbox[3] - tables[table_num].bbox[3]
                upper_side = element.y1
                # �ӱ�����ȡ��Ϣ
                table = extract_table(pdf_path, pagenum, table_num)
                # ������Ϣת��Ϊ�ṹ���ַ�����ʽ
                table_string = table_converter(table)
                # �����ַ���׷�ӵ��б���
                text_from_tables.append(table_string)
                page_content.append(table_string)
                # ����־����ΪTrue���ٴα��������
                table_extraction_flag = True
                # ������Ϊ��һ��Ԫ��
                first_element = False
                # ���ı��͸�ʽ�б������ռλ��
                page_text.append('table')
                line_format.append('table')

            # ��������Ƿ��Ѿ���ҳ������ȡ�˱�
            if element.y0 >= lower_side and element.y1 <= upper_side:
                pass
            elif not isinstance(page_elements[i + 1][1], LTRect):
                table_extraction_flag = False
                first_element = True
                table_num += 1

    # �����ֵ�ļ�
    dctkey = 'Page_' + str(pagenum)
    # ��list���б����Ϊҳ����ֵ
    text_per_page[dctkey] = [page_text, line_format, text_from_images, text_from_tables, page_content]

# �ر�pdf�ļ�����
pdfFileObj.close()

# ɾ���Ѵ����Ĺ����ļ�
os.remove('cropped_image.pdf')
os.remove('PDF_image.png')

# ��ʾҳ������
result = ''.join(text_per_page['Page_0'][4])
print(result)