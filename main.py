import json
from pathlib import Path

from random_msgs import (
    random_msg1,
    random_msg2,
    random_msg3,
    random_msg4,
    random_msg5,
    random_msg6,
    random_msg7,
)


def main():
    string = 'да'
    
    while string.lower() == 'да':
        
        question = input(random_msg1())
        if question.lower() == 'да':
            continue
        elif question.lower() == 'нет':
            break
        
        keywords, unknownwords = extract_keywords(question)
        
        definitions = find_definitions(keywords)
        
        show_info(definitions)
        
        learn_new_words(unknownwords)        
        
        string = input(random_msg2())
    else:
        print(random_msg3())


def extract_keywords(question):
    """Функция extract_keywords определяет ключевые слова в предложении."""
    symbols = [
        ',', '.', '?', '!', '@', '#', '$', '%', '^', '&', '*',
        '/', '\\', '|', '~', '`', '-', '+', '=', '"', "'", '№', ';', ':',
        '(', ')', '()', '<', '>',
        ]
    try:     
        new_dict = load_definitions(); new_list = load_filters()
        question = question.lower().strip()

        for symbol in symbols:
            question = question.replace(symbol, '') if symbol in question else question
        parts_1 = [el for el in question.split()]      
        
        parts = [el for el in parts_1 if el not in new_list]      

        keywords = [k for k in parts if k in new_dict]

        unknownwords = [n for n in parts if n not in new_dict]
    except FileNotFoundError:
        print('Файл не найден!')
        return [], []
    except UnboundLocalError:
        print('Не удалось определить значения!')
        return [], []
    except (ValueError, KeyError, TypeError) as e:
        print(f'Возникла ошибка: {e}')
        
    return keywords, unknownwords      
    
def load_definitions():
    """Функция load_definitions создает словарь."""
    path = Path('library.json')
    contents = path.read_text()
    dict_def = json.loads(contents)

    return dict_def

def load_filters():
    """Функция load_filters создает список для слов конструкторов."""
    path = Path('fillers.json')
    contents = path.read_text()
    words_constructors = json.loads(contents)
              
    return words_constructors 

def find_definitions(keywords):
    """Функция find_definitions возвращает список значений исходя из ключевых слов."""
    try:
        if keywords:
            new_dict = load_definitions() 
            definitions = {k:new_dict.get(k) for k in keywords if k in new_dict}
        else:
            print("Не удалось определить слова.")
            return []
    except FileNotFoundError:
        print("Файл library.json не найден. Запустите init_data.py.")
    except (ValueError, KeyError, TypeError) as e:
        print(f"Возникла ошибка: {e}")
        return []
            
    return definitions           

def show_info(definitions):
    """Показывает информацию пользователю."""
    if definitions:
        for key,val in definitions.items():
            print(f"\t{key.capitalize()} - {val}")
    
def learn_new_words(unknownwords):
    """Функция learn_new_words просит у пользователя дать определения неопознанным словам."""
    try:
        path = Path('library.json')
        dict_ks = json.loads(path.read_text())
        changed = False 
        
        if unknownwords:  
            for key in unknownwords:
                print(f'\n{random_msg4()} {key.capitalize()}')
                answer = input(f"Хотите рассказать мне что такое '{key.capitalize()}'? (да/нет) ")
                if answer.lower() == 'да':
                    print(f"{random_msg5()} '{key.capitalize()}'")
                    dict_ks[key] = input(f"Определение слову '{key.capitalize()}': ")
                    print(random_msg6())
                    changed = True
                else:
                    print(random_msg7())
            
            if changed:
                path.write_text(json.dumps(dict_ks))
    except FileNotFoundError:    
        print("Файл library.json не найден. Запустите init_data.py.")
    except (ValueError, KeyError, TypeError) as e:
        print(f"Возникла ошибка: {e}")
            
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nВозвращайтесь!")