import os
import pypdf


def main(name_file):
    new_name = name_file[:-4] + '_new.pdf'
    pdf = pypdf.PdfReader(name_file)
    num_pages = pdf.get_num_pages()
    new_pdf = pypdf.PdfWriter()
    for i in range(num_pages):
        page = pdf.get_page(i)
        print(f'Номер страницы {i}')
        images_lst = []
        for p in page['/Resources']['/XObject']:
            if page['/Resources']['/XObject'][p]['/Width'] > 1400 \
                    and page['/Resources']['/XObject'][p]['/Height'] > 1900:
                images_lst.append(p)
        for img in images_lst:
            print(img)
            del page['/Resources']['/XObject'][img]
        new_pdf.add_page(page)

    with open(new_name, 'wb') as output:
        new_pdf.write(output)


if __name__ == '__main__':
    main('C:\\1C\\SDN.pdf')
