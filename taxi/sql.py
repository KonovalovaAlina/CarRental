SQL_GET = """
SELECT * FROM {};"""
SQL_GET_MAX_ID = """
SELECT MAX(id) FROM {};"""
SQL_DELETE = """
delete from {0} where id = {1};"""

SQL_ADD_CLIENT = """
insert into client
    (id, client_name, client_phone_number)
values
       ({0}, '{1}','{2}');"""
SQL_ADD_STUFF = """
insert into employee
    (id, employee_name, birthday_date)
values
       ({0},'{1}','{2}');"""

SQL_ADD_REQUEST = """
insert into requests
    (id, requisites, name_manager, start_date_r, finish_date_r)
    values
           ({0},{1},{2},'{3}','{4}');
insert into car_requests
    (requests_id, car_type, quantity)
    values
           ({0},{5},{6});
update car set is_available=FALSE where id={5};
"""

SQL_ADD_CAR_ACCESSORS = """
insert into car_accessories
    (accessories_name, accessories_cost)
values
       ('{0}',{1});"""

SQL_ADD_CONTRACTS = """
insert into contracts
    (id, contract_data, cost)
     values
            ({0},{1},{2});"""

SQL_ADD_REQUEST_ACCESSORS = """
insert into accessories_requests
    (requests_id, accessories, quantity)
    values ({0},'{1}',{2});"""

SQL_ADD_CAR = """
insert into car
    (id, car_number, car_model, car_color, car_cost, is_available)
select {0},'{1}','{2}','{3}', {4}, TRUE where not EXISTS
    (select car_number from car where car_number = '{1}');
"""

# получение списка клиентов, бравших определенную машину на прокат

SQL_GET_INFO_BY_CAR = """
select client_name, client_phone_number from client c
inner join requests r on c.id = r.requisites
inner join car_requests cr on r.id = cr.requests_id
inner join car on cr.car_type = car.id
where car.id={0};
"""

# определение количества своодных машин(которые не в прокате)
SQL_GET_FREE_CARS = """
select * from car
where is_available = TRUE;"""

# получение справочной информации о клиенте
SQL_GET_CLIENT_INFO = """
select * from client
where id={0};"""

SQL_GET_REQUEST_INFO = """
select r.id, cl.client_name, e.employee_name, r.start_date_r, r.finish_date_r  from requests r
inner join client cl on cl.id = r.requisites
inner join employee e on e.id = r.name_manager
;"""

SQL_GET_CONTRACT_INFO = """
select cc.id, cl.client_name, e.employee_name, r.start_date_r, r.finish_date_r, cc.cost from contracts cc
inner join  requests r on r.id = contract_data
inner join client cl on cl.id = r.requisites
inner join employee e on e.id = r.name_manager;"""


SQL_GET_MANAGER_FROM_ID = """
select employee_name from employee e
where e.id = {0};"""

# установление ФИО менеджера, оформлявшего заявку с определенным клиентом
SQL_GET_MANAGER_WITH_REQUEST = """
select employee_name from employee e
inner join requests r on e.id = r.name_manager
left join client c on r.requisites = c.id
where c.id = {0};"""

# счет за прокат автомобиля (выбираем для какой заявки нужно узнать счет, выводим номер контракта, имя менеджера,
#  имя клиента, модель и номер автомобиля,
#  стоимость(состоит из количества дней*стоимость проката за сутки+количество аксессуаров*стоимость аксессуара))
# в одной заявке можно оформить несколько машин, возможно стоит вывести суммарную стоимость проката для одной заявки
SQL_GET_COST_BY_REQUEST = """
select r.id, e.employee_name, cl.client_name, c2.car_model, c2.car_number,
       coalesce((c2.car_cost*(r.finish_date_r-r.start_date_r)+coalesce(ar.quantity,0)*coalesce(ca.accessories_cost,0)),0) price from contracts c
inner join requests r on c.contract_data = r.id
inner join car_requests cr on r.id = cr.requests_id
left join car c2 on cr.car_type = c2.id
left join client cl on r.requisites = cl.id
left join employee e on r.name_manager = e.id
left join accessories_requests ar on cr.requests_id = ar.requests_id
left join car_accessories ca on ar.accessories = ca.accessories_name
where r.id={0};"""

# --sотчет о работе компании за месяц
#   --сколько заявок было оформлено за месяц
SQL_GET_REPORT = """
select count(id) from requests
where start_date_r>='{0}' and finish_date_r<='{1}';"""

#  --какие машины брали в аренду за месяц
SQL_CARS_FOR_RANGE = """
select distinct car_number,car_model from car
right join car_requests cr on car.id = cr.car_type
inner join requests r on cr.requests_id = r.id
where start_date_r>='{0}' and finish_date_r<='{1}';"""

# --какую сумму заработала компания за месяц
SQL_GET_PROFIT_FOR_RANGE = """
select coalesce(sum(c.car_cost*(r.finish_date_r-r.start_date_r)+coalesce(ar.quantity,0)*coalesce(ca.accessories_cost,0)),0) price from requests r
inner join car_requests cr on r.id = cr.requests_id
inner join car c on cr.car_type = c.id
left join accessories_requests ar on cr.requests_id = ar.requests_id
left join car_accessories ca on ar.accessories = ca.accessories_name
where start_date_r>='{0}' and finish_date_r<='{1}';"""
