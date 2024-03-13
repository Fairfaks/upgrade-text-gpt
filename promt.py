import os
import openai

# Указываем API ключ для OpenAI
API_KEY = 'свой'
PROXY = 'http://ну ты понял'

# Устанавливаем API ключ и прокси в переменных окружения
os.environ["OPENAI_API_KEY"] = API_KEY
os.environ["http_proxy"] = PROXY
os.environ["https_proxy"] = PROXY

# Создаем клиент для работы с API
openai.api_key = API_KEY

def main():
    # Получаем изначальный текст для обработки
    file_text = 'old.txt'
    text = read_file(file_text)
    extracted_text = extract_text_with_html(text)

    # Получаем промт для ChatGPT
    file_promt = 'promt.txt'
    promt = read_file(file_promt)

    # Получаем ключи
    file_keywords = 'keywords.txt'
    keywords = get_keywords(file_keywords)

    # Печатаем извлеченный текст для проверки
    print("Задача для ChatGPT:")
    print(promt, extracted_text)
    print('=====================')

    try:
        # Обрабатываем текст с использованием ChatGPT
        recomendation = process_text_with_chatgpt(promt + extracted_text)

        # Из полученных рекомендаций выбираем маркерный список
        improvements = get_improvements_from_text(recomendation)
        if improvements:
            print(improvements)
            print('=====================')
        else:
            print('\n==== Рекомендации не получены ====\n')

        # Запрос на улучшение текста с рекомендациями и ключевыми словами
        query = '\nПерепиши текст используя ключевые слова и рекомендации\n'
        query = query + keywords + '\n' + recomendation  + '\n' + extracted_text
        print(query)
        print('=====================')
        improved_text = process_text_with_chatgpt(query)

        # Сохраняем улучшенный текст в файл
        with open('new.txt', 'w', encoding='utf-8') as file:
            file.write(recomendation + '\n' + keywords + '\n' + improved_text)

        print("\nУлучшенный текст сохранен в файл new.txt")

    except Exception as e:
        print("Произошла ошибка при обработке текста:", str(e))




def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text_with_html(text):
    return text.split('<start>')[1].split('<end>')[0]

def get_keywords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        keywords = [line.strip() for line in file.readlines()]
        return '\n'.join(keywords)

def process_text_with_chatgpt(text):
    # Отправляем текст на обработку с помощью ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a customer"},
            {"role": "user", "content": text}
        ]
    )
    new_text = response['choices'][0]['message']['content']
    return new_text.strip()

def get_improvements_from_text(text):
    # Выбираем из текста маркерный список
    improvements = []
    for t in text.split('\n'):
        if t.strip().startswith("-"):
            improvements.append(t.strip())
    return '\n'.join(improvements)


if __name__ == "__main__":
    main()
    # Эта строка блокирует закрытие окна до нажатия Enter
input("Нажмите Enter для завершения...")
