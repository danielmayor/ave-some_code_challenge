from pathlib import Path
import sys, getopt

def get_file_content(input_file):
    with open(input_file, 'rb') as f:
      content = f.read()
      f.close()
      content = content.decode('utf-16')
      content = content.split('\r\n')
    return content

def process_file(file_content):
    truncated_file_content = []
    for line in file_content:
        if line.strip() != '':
            lista = line.split(' : ')
            if lista[0].endswith('-Password') or lista[0].endswith('-Key') or lista[0].endswith('-ClientSecret'):
                lista[1] = truncate(lista[1])
            elif 'password=' in lista[1]:
                lista[1] = replace_value(lista[1],'password=',',')
            elif 'AccountKey=' in lista[1]:
                lista[1] = replace_value(lista[1],'AccountKey=',';')
            truncated_lista = ' : '.join(lista)
            truncated_file_content.append(truncated_lista)
    return truncated_file_content

def truncate(value):
    truncated = value[:5] + '...' + value[-5:]
    return truncated

def replace_value(value, key, separator):
    stage1 = value.split(separator)
    stage3 = []
    for element in stage1:
        if key in element:
            stage2 = element.split(key)
            stage2[1] = truncate(stage2[1])
            element = key.join(stage2)
        stage3.append(element)
    replaced = separator.join(stage3)
    return replaced

def generate_output_file(processed, name):
    content_to_write = ''
    for line in processed:
        content_to_write += line + '\n'
    f = open('obfuscated_' + name, 'w', encoding='utf-16')
    f.write(content_to_write)
    f.close()

def main(arg):
    if arg:
        file_path = Path(arg[0])
        file_content = get_file_content(file_path)
        processed_content = process_file(file_content)
        generate_output_file(processed_content, file_path.name)
        print('File generated: ' + 'obfuscated_' + file_path.name)
    else:
        print('Syntax:')
        print('aveva.py <input_file>')

if __name__ == "__main__":
    main(sys.argv[1:])
