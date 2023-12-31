# bewise_test_fastapi
Веб сервис на FastAPI: принимает на вход POST запросы с содержимым вида {"questions_num": integer}, запрашивает с публичного API (англоязычные вопросы для викторин),  сохраняет их в базе данных PostgreSQL ( если в БД уже есть этот вопрос, выполняет доп. запросы, пока не получит уникальный). Сервис возвращает предыдущий вопрос или пустой объект.

# Инструкция по развёртыванию проекта (для Ubuntu)
1. cкачать исходный код проекта по ссылке: [git clone https://github.com/Sana451/bewise_test_fastapi.git](https://github.com/Sana451/bewise_test_fastapi.git)
3. перейти в папку с проектом: `cd bewise_test_fastapi/`
4. убедиться, что запущен docker и установлен docker compose
5. произвести сборку проекта командой: `docker compose build`
6. создать и запустить контейнеры командой: `docker compose up`

# Проверка работы API
Перейти по url адресу автоматической документации swagger:  
[http://127.0.0.1:8010/docs#/default/load_and_return_question_questions__post]  
или выполнить POST запрос вручную по адресу [http://127.0.0.1:8010/questions/] с телом запроса: {"questions_num": N: int} (например: `{"questions_num": 1}`),  где N-количесство вопросов, которое сервис запросит у публичного API и сохранит в базе данных)
Если база данных при выполнении запроса будет пустая (например при первом запросе), то ответом на запрос будет JSON объект вида:  
   **{"id": null,  
  "question": null,  
  "answer": null,  
  "created_at": null,  
  "added_at": null}**,  
при последующих запросах будет возвращён предыдущий сохранённый в базе данных JSON объект вида:  
***{"id": 61664,  
  "question": "In both an Iron Maiden hit song",  
  "answer": "666",  
  "created_at": "2022-12-30T19:04:15.374",  
  "added_at": "2023-10-14T08:19:47.837626Z"}***  

  # Проверка сохранения данных в базе
  Для того, чтобы убедиться что объекты действительно сохранены в базе данных:   
  войти в терминал docker контейнера базы данных: `psql -U fastapi_celery`,   
  выполнить SQL запрос к таблице *questions*: `SELECT * FROM questions;` 
