# GUI-приложение #

## О приложении ##

Данный проект представляет собой GUI-приложение для визуализации решения транспортной задачи методом потенциалов с 
применением метода северо-западного угла для нахождения опорного плана.

## Реализация ##

Приложение написано на языке программирования ```Python 3.9```, для визуализаици была использована библиотека ```PyQt5```.

## Запуск приложения ##

Для того чтобы установить все пакеты нужно ввести в терминале

```pip install -r requirements.txt```

Для запуска приложения необходимо ввести в консоли

```python -m app.main```

## Работа с приложением ##

После запуска Вы можете увидеть главное окно приложения. Для начала нужно ввести количество поставщиков и потребителей 
и нажать на кнопку "Ввести".

![1](https://github.com/Drozdova-Daria/pictures/blob/main/1.png)

Затем нужно ввести транспортную таблицу и также нажать кнопку "Ввести".

![2](https://github.com/Drozdova-Daria/pictures/blob/main/2.png)

В итоге получаем решение задачи. Первая таблица показывает опорный план, полученный методом северо-западного угла, 
вторая таблица - решение задачи, полученное методом потенциалов

![3](https://github.com/Drozdova-Daria/pictures/blob/main/3.png)

Чтобы увидеть значения, полученные на каждой итерации алгоритма, необходимо нажать на кнопку "+ Показать шаги"

![4](https://github.com/Drozdova-Daria/pictures/blob/main/4.png)

## Команда разработки ##

Дроздова Дарья

Медведева Таисия
