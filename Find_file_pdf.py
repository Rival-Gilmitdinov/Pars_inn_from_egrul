import requests
import time
import os
from qwe import cookies, headers
from Work_excel import sp


class Find_pdf_file():
    def query(self, table):
        '''Функция по отправлению инн из excel файла, отправления запросов на сайт
        ЮГРЛ с целью получения пдф файла с данными об организации'''
        session = requests.Session()
        # Проходим циклом по списку из значений инн
        for value in table:
            if self.chek(value) == True:
                continue
            json = {'vyp3CaptchaToken': '',
                        'page': '',
                        'query': f'{value}',
                        'region': '',
                        'PreventChromeAutocomplete': ''
                        }
            #Отправляем запрос в поисковую строку
            response = session.post(url='https://egrul.nalog.ru/', json=json).json()
            # Получаем результаты
            get_value = session.get(url=f'https://egrul.nalog.ru/search-result/{response["t"]}')
            token = get_value.json()['rows'][0]['t']
            # Создаем запрсо для обозначения статуса в будущем готовности документа к скачиванию
            first_query = session.get(url=f'https://egrul.nalog.ru/vyp-request/{token}')
            first_query_token = first_query.json()['t']
            count = 0
            while count < 5:
                file = session.get(url=f'https://egrul.nalog.ru/vyp-status/{first_query_token}', timeout=20)
                time.sleep(5)
                if file.json()['status'] == 'ready':
                    print(file.json()['status'])
                    break
                else:
                    print('NO')
                count += 1
            if file.json()['status'] == 'ready':
                # Отправляем запрос для получения файла
                file_pdf = session.get(url=f'https://egrul.nalog.ru/vyp-download/{token}', headers=headers)
            self.save_document(file_pdf, value)


    def save_document(self, file, inn):
        """Функция по сохранению пдф файла
        file - полученный файл
        inn - номер инн, спарсенный из excel"""
        file_path = os.path.join('saving_pdf', f'{inn}_result_search_file.pdf')
        with open(file_path, mode='wb') as file_pdf:
            file_pdf.write(file.content)

    def chek(self, znachenie):
        """Функция по проверке, есть ли уже пдф файл с значением инн,которое нужно спарсить"""
        flag = False
        dir = 'C:\Python\pythonProject\\2025\work_inn\saving_pdf'
        for file in os.listdir(dir):
            if str(znachenie) in file:
                flag = True
        return flag


pdf_files = Find_pdf_file()
# pdf_files.query(sp[0])