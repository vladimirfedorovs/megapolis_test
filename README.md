# Тест SQL

На основе таблиц базы данных, напишите SQL код, который возвращает необходимые результаты
Пример: 

Общее количество товаров
```sql
select count (*) from items
```

## Структура данных

Используемый синтаксис: Oracle SQL или другой

| Сustomer       | Description           |
| -------------- | --------------------- |
| customer\_id   | customer unique id    |
| customer\_name | customer name         |
| country\_code  | country code ISO 3166 |

| Items             | Description       |
| ----------------- | ----------------- |
| item\_id          | item unique id    |
| item\_name        | item name         |
| item\_description | item description  |
| item\_price       | item price in USD |

| Orders       | Description                 |
| ------------ | --------------------------- |
| date\_time   | date and time of the orders |
| item\_id     | item unique id              |
| customer\_id | user unique id              |
| quantity     | number of items in order    |

| Countries     | Description           |
| ------------- | --------------------- |
| country\_code | country code          |
| country\_name | country name          |
| country\_zone | AMER, APJ, LATAM etc. |


| Сonnection\_log         | Description                           |
| ----------------------- | ------------------------------------- |
| customer\_id            | customer unique id                    |
| first\_connection\_time | date and time of the first connection |
| last\_connection\_time  | date and time of the last connection  |

## Задания

### 1) Общее количество покупателей

| **CustomerCountDistinct** |
| ----------------------------- |
| #                             |

```sql
select count (*) from customer
```

### 2) Количество покупателей из Италии и Франции

| **Country_name** | **CustomerCountDistinct** |
| ------------------------- | ----------------------------- |
| France                    | #                             |
| Italy                     | #                             |

```sql
select country_name, count(*) from customer a
left join countries b on a.country_code = b.country_code
where country_name in ('France','Italy')
group by country_name
```

### 3) ТОП 10 покупателей по расходам

| **Customer_name** | **Revenue** |
| ---------------------- | ----------- |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |

```sql
select top(10)
customer_name, sum(item_price*quantity) revenue
from orders a
left join items b on a.item_id = b.item_id
left join customer c on a.customer_id = c.customer_id
group by customer_id, customer_name --группируем по id на случай совпадающих имен
order by revenue desc
```

### 4) Общая выручка USD по странам, если нет дохода, вернуть NULL

| **Country_name** | **RevenuePerCountry** |
| ------------------------- | --------------------- |
| Italy                     | #                     |
| France                    | NULL                  |
| Mexico                    | #                     |
| Germany                   | #                     |
| Tanzania                  | #                     |

```sql
select country_name, sum(item_price*quantity) RevenuePerCountry
from countries a
left join customer b on a.country_code = b.country_code
left join orders c on b.customer_id = c.customer_id
left join items d on c.item_id = d.item_id
group by country_name
```

### 5) Самый дорогой товар, купленный одним покупателем

| **Customer\_id** | **Customer\_name** | **MostExpensiveItemName** |
| ---------------- | ------------------ | ------------------------- |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |

```sql
with pre as (
select a.customer_id, customer_name,  item_name,
row_number() over(partition by a.customer_id, customer_name order by item_price desc) rn
from customer a
left join orders b on a.customer_id = b.customer_id
left join items c on b.item_id = c.item_id
)
select customer_id, customer_name, item_name MostExpensiveItemName
from pre 
where rn = 1
```

### 6) Ежемесячный доход

| **Month (MM format)** | **Total Revenue** |
| --------------------- | ----------------- |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |

```sql
select trunc(date_time, 'mm') report_month, sum(item_price*quantity) Total_Revenue
from orders a 
left join items b on a.item_id = b.item_id
group by trunc(date_time, 'mm')
-- если имеется в виду, что нужно выводить только номер месяца, то trunc(date_time, 'mm') нужно заменить на extract(month from date_time)
```

### 7) Общий доход в MENA

| **Total Revenue MENA** |
| ---------------------- |
| #                      |

```sql
-- не разобрался, что такое общий доход в MENA, вывел просто общий доход за все время
select sum(item_price*quantity) Total_Revenue_MENA
from orders a 
left join items b on a.item_id = b.item_id
```

### 8) Найти дубликаты

Во время передачи данных произошел сбой, в таблице orders появилось несколько 
дубликатов (несколько результатов возвращаются для date_time + customer_id + item_id). 
Вы должны их найти и вернуть количество дубликатов.

```sql
select date_time, customer_id, item_id, count(*) cnt
from orders
group by date_time, customer_id, item_id
having count(*) > 1 
```
