"""
Удаление водяных знаков из файлов PDF
"""
import os
import pypdf
from datetime import datetime
from Crypto.Cipher import AES

# Длина названия водяного знака. Регулиуется подбором
LONG_IMAGE = 12


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
        try:
            for p in page['/Resources']['/XObject']:
                # if page['/Resources']['/XObject'][p]['/Width'] > 1400 \
                #         and page['/Resources']['/XObject'][p]['/Height'] > 1900:
                if len(p) > LONG_IMAGE:
                    images_lst.append(p)
            for img in images_lst:
                print(f"Удаляем {img}")
                del page['/Resources']['/XObject'][img]
            new_pdf.add_page(page)
        except:
            print(f'В файле {name_file} страница {i + 1} нет знаков!')
            continue

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
    type_input = input('Введите путь к папкам или оставьте текущую - Enter\n')
    if len(type_input) == 0:
        print(os.getcwd())
        list_files = watch_files(os.getcwd())
    elif os.path.isdir(type_input):
        print(type_input)
        list_files = watch_files(os.path.abspath(type_input))
    else:
        print("Нет такой папки. Введите ешё раз!")
    start_time = datetime.now()
    for file in list_files:
        print(file)
        del_watermark(file)
    print(f"Все сделано за {(datetime.now() - start_time).__str__().split('.')[0]} секунд")
