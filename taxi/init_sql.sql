create DATABASE DB;

--клиент
create table client
(
    id int primary key,
    client_name text not null,
    client_phone_number text not null unique
);

--сотрудник
create table employee
(
    id int primary key,
    employee_name text not null,
    birthday_date date not null
);

--автомобиль
create table car
(
    id int primary key,
    car_number text not null unique,
    car_model text not null,
    car_color text not null,
    car_cost int not null,
    is_available boolean not null
);

--аксессуары к автомобилю
create table car_accessories
(
    accessories_name text primary key,
    accessories_cost int not null
);

--заявка
create table requests
(
    id serial primary key,
    requisites int references client(id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
    name_manager int references employee(id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
    start_date_r date not null,
    finish_date_r date not null,
check(finish_date_r >= start_date_r)
);

--связь автомобиля по заявке
create table car_requests
(
    requests_id int references requests(id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
    car_type int references car(id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
    quantity int not null
);

--связь аксессуаров по заявке
create table accessories_requests
(
    requests_id int references requests(id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
    accessories text references car_accessories(accessories_name) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
    quantity int
);

--договор
create table contracts
(
    id serial primary key,
    contract_data int references requests(id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
    cost int not null
);

--права администратора БД(мои)
CREATE USER admin WITH password 'admin';
GRANT SELECT, UPDATE, INSERT, DELETE ON client TO admin;
GRANT SELECT, UPDATE, INSERT, DELETE ON employee TO admin;
GRANT SELECT, UPDATE, INSERT, DELETE ON car TO admin;
GRANT SELECT, UPDATE, INSERT, DELETE ON car_accessories TO admin;
GRANT SELECT, UPDATE, INSERT, DELETE ON requests TO admin;
GRANT SELECT, UPDATE, INSERT, DELETE ON contracts TO admin;

--права директора компании
CREATE USER director WITH password 'director';
GRANT SELECT ON client TO director;
GRANT SELECT, INSERT, DELETE ON employee TO director;
GRANT SELECT, INSERT, DELETE ON car TO director;
GRANT SELECT, INSERT, DELETE ON car_accessories TO director;
GRANT SELECT, UPDATE, INSERT, DELETE ON car_requests TO director;
GRANT SELECT, UPDATE, INSERT, DELETE ON accessories_requests TO director;
GRANT SELECT ON requests TO director;
GRANT SELECT ON contracts TO director;

--права администратора(менеджера)
CREATE USER manager WITH password ' manager ';
GRANT SELECT, UPDATE, INSERT, DELETE ON client TO manager;
GRANT SELECT ON employee TO manager;
GRANT SELECT, UPDATE ON car TO manager;
GRANT SELECT ON car_accessories TO manager;
GRANT SELECT, UPDATE, INSERT, DELETE ON requests TO manager;
GRANT SELECT, UPDATE, INSERT, DELETE ON contracts TO manager;
GRANT SELECT, UPDATE, INSERT, DELETE ON accessories_requests TO manager;
GRANT SELECT, UPDATE, INSERT, DELETE ON car_requests TO manager;

--пример заполнения данных
insert into client
    (id, client_name, client_phone_number)
values
       (1, 'Сидоров Евгений Петрович','+78005553535'),
       (2,'Василенко Михаил Антонович','+79631787212'),
       (3,'Олегов Егор Олегович','+79821154343'),
       (4,'Дуболомов Артем Леонидович','+79431712601'),
       (5,'Карасев Сергей Борисович','+79523711414');

insert into employee
    (id, employee_name, birthday_date)
values
       (1,'Иванов Ян Вадимович','1987-12-12'),
       (2,'Градиентов Петр Афанасьевич','1975-04-14'),
       (3,'Зюзин Егор Игнатович','1975-05-05');

insert into car
    (id, car_number, car_model, car_color, car_cost, is_available)
values
       (1,'Е386ЕО','Mercedes GLE','Серый', 5000,TRUE),
       (2,'Б171ГД','Skoda Rapid','Черный',2000, TRUE),
       (3,'О111ОО','Ford Mondeo','Синий',2000, TRUE),
       (4,'А127АО','Toyota Camry','Белый',4000, TRUE),
       (5,'Л343ЛА','Nissan Qashqai','Красный',3000, TRUE);

insert into car_accessories
    (accessories_name, accessories_cost)
values
       ('Детское кресло',200),
       ('GPS-навигатор',100),
       ('Антирадар',100),
       ('Видеорегистратор',100);

insert into requests
    (id, requisites, name_manager, start_date_r, finish_date_r)
    values
           (1,2,1,'2021-11-20','2021-11-22'),
           (2,4,3,'2021-11-15','2021-11-16'),
           (3,1,2,'2021-12-12','2021-12-17');

insert into car_requests
    (requests_id, car_type, quantity)
    values
           (1,1,1),
           (1,2,2),
           (2,3,1),
           (3,4,1);

insert into accessories_requests
    (requests_id, accessories, quantity)
    values
           (1,'Детское кресло',2),
           (2,'Видеорегистратор',1),
           (2,'Антирадар',1),
           (3,'GPS-навигатор',1);

insert into contracts
    (id, contract_data, cost)
     values
            (4,4,13400),
            (2,2,2000),
            (3,3,6100);
--пример заполнения данных

--оформление менеджером заявки клента
  --вносим информацию о клиенте
insert into client
    (id, client_name, client_phone_number)
    select 6, 'Яковлева Екатерина Юрьевна','+78005554763' where not EXISTS
    (select client_phone_number from client where client_phone_number = '+78005554763');
  --проверяем, какие автомобили свободны
select id from car where is_available=TRUE;
  --оформляем заявку
insert into requests
    (id, requisites, name_manager, start_date_r, finish_date_r)
    values
           (4,6,1,'2021-12-20','2021-12-22');
insert into car_requests
    (requests_id, car_type, quantity)
    values
           (4,4,1);
insert into accessories_requests
    (requests_id, accessories, quantity)
    values (4,'Видеорегистратор',1);
update car set is_available=FALSE where id_car=4;
