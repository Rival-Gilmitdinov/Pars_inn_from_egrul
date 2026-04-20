import requests
import time
import os
from qwe import headers




class Find_pdf_file():
    def __init__(self):
        self.error_response = {}


    def query(self, table, path_dir, list_inn_from_postgre) -> None :
        """Функция по удалению старых данных из папки и по отправлению инн из excel файла, отправления запросов на сайт
        ЮГРЛ с целью получения пдф файла с данными об организации
        Arguments:
            table - list
                Список с инн, по которым пользователь хочет получить данные"""
        print(f'в постгрессе есть данные по инн, в результате запроса список составляет: {list_inn_from_postgre}')
        session = requests.Session()
        # Проходим циклом по списку из значений инн
        for value in table:
            print(value)
            try:
                if value in set(list_inn_from_postgre):
                    continue
            except:
                pass
            json = {'vyp3CaptchaToken': '',
                        'page': '',
                        'query': f'{value}',
                        'region': '',
                        'PreventChromeAutocomplete': ''
                        }
            #Отправляем запрос в поисковую строку
            response = session.post(url='https://egrul.nalog.ru/', json=json).json()
            # Получаем результаты
            try:
                get_value = session.get(url=f'https://egrul.nalog.ru/search-result/{response["t"]}')
            except:
                self.error_response.setdefault(value, 'Не удается получить ответ от сервиса')
                print(f'Не удается получить ответ от сервиса по {value} инн')
                continue
            token = get_value.json()['rows'][0]['t']
            # Создаем запрсо для обозначения статуса в будущем готовности документа к скачиванию
            first_query = session.get(url=f'https://egrul.nalog.ru/vyp-request/{token}')
            first_query_token = first_query.json()['t']
            count = 0
            while count < 5:
                file = session.get(url=f'https://egrul.nalog.ru/vyp-status/{first_query_token}', timeout=20)
                time.sleep(0.5)
                if file.json()['status'] == 'ready':
                    print(file.json()['status'])
                    break
                else:
                    print('NO')
                count += 1
            if file.json()['status'] == 'ready':
                # Отправляем запрос для получения файла
                file_pdf = session.get(url=f'https://egrul.nalog.ru/vyp-download/{token}', headers=headers)
            self.save_document(file_pdf, value, path_dir)



    def save_document(self, file, inn, path_dir) -> None:
        """Метод по сохранению пдф файла
        Arguments:
            file - полученный файл
            inn - номер инн, спарсенный из excel"""
        file_path = os.path.join(path_dir, f'{inn}_result_search_file.pdf')
        with open(file_path, mode='wb') as file_pdf:
            file_pdf.write(file.content)


    def delete_old_files(self, path_dir) -> None:
        """Метод по удалению файлов из папки"""
        for file in os.listdir(path_dir):
            if 'pdf' in file:
                file_path = os.path.join(path_dir, file)
                os.remove(file_path)


