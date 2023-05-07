import sys
import pdfplumber
import argparse
from tqdm import tqdm
from os import sep

def pdf_path(value):
    from os.path import exists

    if '.pdf' not in value:
        raise ValueError('Required pdf file only')
    
    elif not exists(value):
        raise ValueError('Pdf file does not exists')
    
    return value


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_pdf', dest='input_pdf', type=pdf_path, required=True,
        help="Input pdf file for text extraction",
    )
    parser.add_argument('--start_page', type= int, required= True, help='Start page')
    parser.add_argument('--end_page', type= int, required=True, help='End page')
    parser.add_argument('--output_folder', type= str, default='./output',  help='Output file name prefix')
    args = parser.parse_args()
    
    file_name = args.input_pdf.split('.pdf')[0]

    with pdfplumber.open(args.input_pdf) as pdf:

        if args.start_page > args.end_page:
            print('Try again with correct value i.e start_page < end_page')
            sys.exit()

        elif args.end_page > len(pdf.pages):
            print('End page is greater than no. of pages in this file {f}')
            sys.exit()
        
        for page_nummber in tqdm(range(args.start_page, args.end_page + 1)):
            data_page = pdf.pages[page_nummber]
            text_data = data_page.extract_text_simple(x_tolerance=3, y_tolerance=3)

            output_template = f'{args.output_folder}{sep}{file_name}_pdf_page_{page_nummber}.txt'
            with open(output_template, 'w', encoding='utf-8') as f:
                f.writelines(text_data)

