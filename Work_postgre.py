import psycopg2
from sqlalchemy import create_engine, inspect
from config import user, password, host, db, port
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, Session
from datetime import date, timedelta

engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')
Base = declarative_base()


class Inn(Base):
    __tablename__ = 'data_on_inn'
    id: Mapped[int] = mapped_column(primary_key=True)
    inn_company: Mapped[str | None]
    name: Mapped[str | None]
    capital: Mapped[str | None]
    activity: Mapped[str | None]
    time_created: Mapped[date] = mapped_column(default=date.today())

inspector = inspect(engine)
if not inspector.has_table('data_on_inn'):
    Base.metadata.create_all(bind=engine)


class Append_table_postrge():
    def app(self, data_value, error_type, error_data) -> None:
        """Метод по удалению старых данных и записи новых данных в базу данных
        Parameters:
            spisok: list
                Список из словарей с парсенными данными
            list_inn: list
                Список с данными инн,по которым пользователю нужно данные
            error_type - dict
                словарь с неверными значениями и текстом ошибки
            error_data - dict
                словарь с неверными значениями и текстом ошибки"""
        with Session(engine) as session:
            target_date = date.today() - timedelta(days=10)
            old_data = session.query(Inn).filter(Inn.time_created < target_date)
            old_data.delete(synchronize_session=False)
            session.commit()
            n = 0
            print(data_value)
            print(chek.chek_data_from_postgre()[1])
            for value in data_value:
                if str(value['инн']) in chek.chek_data_from_postgre()[1]:
                    continue
                data = Inn(inn_company=f'{int(value["инн"])}', name=f'{value["Полное наименование на русском языке"]}', capital=f'{value["Сведения об уставном капитале / складочном капитале / уставном фонде / паевом фонде"]}',
                           activity=f'{value["Сведения об основном виде деятельности"]}')
                n += 1
                session.add(data)
            session.commit()
            if error_type:
                for key_error, value_error, in error_type.items():
                    if key_error in chek.chek_data_from_postgre()[1]:
                        continue
                    data_error = Inn(inn_company=f'{key_error}', name=f'{value_error}')
                    session.add(data_error)
                    session.commit()
            if error_data:
                for key_error_2, value_error_2, in error_data.items():
                    if key_error in chek.chek_data_from_postgre()[1]:
                        continue
                    data_error_2 = Inn(inn_company=f'{key_error_2}', name=f'{value_error_2}')
                    session.add(data_error_2)
                    session.commit()


class Check_data():
    def chek_data_from_postgre(self) -> list:
        """Метод по проверке данных в базе данных на давность, в итоговый список добавляется только не старые данные"""
        list_inn_from_postgre = []
        target_date = date.today() - timedelta(days=10)
        with Session(engine) as session:
            results = session.query(Inn).filter(Inn.time_created >= target_date).all()
            for value in results:
                # if value.inn_company.isdigit() and len(value.inn_company) == 10:
                list_inn_from_postgre.append(value.inn_company)
        return results, list_inn_from_postgre


    def pars_from_postgre(self, value):
        """Метод по выборке данных из базы данных, по итогу выходит объект постгресса
        Parameters:
            value: int
                Значение инн, по которым пользователю нужна информацию"""
        with Session(engine) as session:
            data_inn = session.query(Inn).filter(Inn.inn_company == str(value)).all()
        return data_inn


chek = Check_data()

