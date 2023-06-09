# EXCHANGER

Тестовое задание для WEB разработчиков:
----------------------------------------------------------------------------------------------------------------
> Предлагается разработать простой симулятор биржи с клиент-серверной архитектурой.
Биржа это такой "сервис" куда можно отправить заявку (ордер) на покупку или продажу какого либо актива. Получив заявку биржа, применяя некую торговую логику, ищет встречную заявку для заключения сделки. Заявка в итоге может быть исполнена, отклонена или же ее можно отменить самому. При выставлении заявки можно ориентироваться на текущие цены данного актива (котировки), для более вероятного исполнения заявки.
Взаимодействие с биржей происходит через торговый терминал, который является клиентом в данной архитектуре, а сама биржа - это сервер.

> ⚡ Для упрощения задачи, реализовывать торговую логику не нужно, исполнение заявок и поток котировок можно симулировать. 
Т.е. при получении заявки сервер делает вид, что некоторое время ищет встречный ордер, и в итоге
дает произвольный ответ исполнена ли заявка или нет.
----------------------------------------------------------------------------------------------------------------

 Условия:
----------------------------------------------------------------------------------------------------------------
> Поддерживает подключение по протоколу websocket нескольких клиентов одновременно, дает им возможность:
* получать информацию о всех своих заявках
* получать текущие котировки
* выставлять заявки
* отменять активные заявки
----------------------------------------------------------------------------------------------------------------
#### <a id="api"></a>API:
Все сообщения имеют общий `JSON` формат:
    
    {
        "messageType": <integer>,
        "message": <object>
    }
* **SubscribeMarketData**
* **UnsubscribeMarketData**
* **PlaceOrder**
* **CancelOrder**
* **SuccessInfo**
* **ErrorInfo**
* **ExecutionReport**
* <a id="web-terminal"></a>**MarketDataUpdate**

Установка & настройка
----------------------------------------------------------------------------------------------------------------
-	Склонировать проект
- Перейти в директорию server
- Создать виртуальное окружение (python -m venv venv)
- Активировать виртуальное окружение (venv/scripts/activate)
- Установить все зависимости из req.txt (pip install -r req.txt)
-	Создать файл .env в корне server и заполнить константы указанные в файле example.env (если не указывать константы для базы данных, то они установятся по дефолту)
>	Если возникнут проблемы с базой данной Postgres, то Django автоматически подключит sqlite3
-	Создать и применить миграции командами (python manage.py makemigrations) & (python manage.py migrate)
-	Создать суперпользователя командой (python manage.py createsuperuser)
- Запустить сервер с помощью <b>daphne</b> (daphne config.asgi:application)
-	Server готов к использованию!
- Вернитесь в корневой каталог и перейдите в client
- Установить необходимые зависимости (npm install)
-	Создать файл .env в корне client и заполнить константы указанные в файле example.env
- Запустить client React (npm start)
- Client готов к использованию!
- Проект развернут!
----------------------------------------------------------------------------------------------------------------

Навигация:

----------------------------------------------------------------------------------------------------------------
-	По адресу 127.0.0.1:8000/api/ открывается автодокументация
-	По адресу 127.0.0.1:8000/admin открывается окно авторизации в админ-панель, в которой можно создать активы для создания заявок (ex. BTC, ETH, BNB ...)
----------------------------------------------------------------------------------------------------------------

Описание реализованного функционала:
----------------------------------------------------------------------------------------------------------------
> <b>NOTICE</b> Для корректной иммитации работы "реальной биржи" у всех API выставлены права AllowAny, для успешного прохождения всех тестов необходимо изменить на нужные права доступа!

> API
* Работа с токенами (создание, верификация, обновление)
* Работа с заявками (Создание заявки/Редактирование заявки)
* Работа с транзакциями (Создание транзакции)
* Работа с активами (Редактирование цены актива, Получение пересечений всех активов (для отображения в тикере), редактирование цены актива (для иммитации реальной биржи))
* Работа с пользователями (Регистрация)
> WS
* Работа с заявками (Получение всех заявок сразу, при добавлении новой заявки её отправка)
* Работа с активами (Получение всех активов, подписка на определенный актив, отписка от актива)

> Client
* Авторизация/Регистрация
* Получение в тикере всех возможных активов
* Автоподписка на определенный актив, при выборе актива
* Автоотписка при смене актива
* Динамическое добавление новой заявки
* Динамическое обновление заявок
* Нотификация в виде alert, при изменении заявки
* Возможность отменять созданную заявку
* Иммитация "реальной биржи" (автообновление случайных активов из списка (BTC, USD, RUB, BNB, ETH, автообновление статуса заявки)
* Тикер отображает актуальные котировки (минимальную и максимальную цену из уже созданных активных заявок)
* Тикер отображает актуальную цену актива
* Валидация формы регистрации, авторизации, тикера

> Server
* Валидация всех данных
* Все сообщения сервера в определенном формате
* Основная часть функционала покрыта тестами
* Сервер поддерживает несколько подключений
* Автоотписка от обновлений актива при дисконекте пользователя
* Поддержка нескольких подписок на обновления активов
