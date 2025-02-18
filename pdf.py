"""
Удаление водяных знаков из файлов PDF
"""
import os
import pypdf
from Crypto.Cipher import AES

# Длина названия водяного знака. Регулиуется подбором
LONG_IMAGE = 12
PROB_DIR = "D:\\Вебинары\\Апейрон\\"


def del_watermark(name_file):
    """Удаление водяного знака одного файла"""
    new_name = name_file[:-4] + '_new.pdf'
    pdf = pypdf.PdfReader(name_file)
    num_pages = pdf.get_num_pages()
    new_pdf = pypdf.PdfWriter()
    for i in range(num_pages):
        page = pdf.get_page(i)
        print(f'Номер страницы {i}')
        images_lst = []
        for p in page['/Resources']['/XObject']:
            # if page['/Resources']['/XObject'][p]['/Width'] > 1400 \
            #         and page['/Resources']['/XObject'][p]['/Height'] > 1900:
            if len(p) > LONG_IMAGE:
                images_lst.append(p)
        for img in images_lst:
            print(f"Удаляем {img}")
            del page['/Resources']['/XObject'][img]
        new_pdf.add_page(page)

    with open(new_name, 'wb') as output:
        new_pdf.write(output)


def watch_files(name_cur) -> list:
    """Поиск всех файлов PDF во всех подпапках"""
    lst_files = []
    for root, dirs, files in os.walk(name_cur):
        for pdf_file in files:
            if pdf_file.endswith('.pdf') and '_new' not in pdf_file:
                lst_files.append(os.path.join(root, pdf_file))
    return lst_files


if __name__ == '__main__':
    #list_files = watch_files(os.getcwd())
    list_files = watch_files(PROB_DIR)
    for file in list_files:
        print(file)
        del_watermark(file)
