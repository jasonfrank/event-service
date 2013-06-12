create table if not exists event (
        id integer primary key autoincrement,
        application_id integer not null,
        event_time integer not null,
        event_type_id integer not null,
        headline varchar(200) not null,
        body varchar(4192)
);

create table if not exists event_entity (
        id integer primary key autoincrement,
        event_id integer unsigned not null,
        entity_type integer not null,
        entity_id integer not null,
        unique (event_id, entity_type, entity_id)
);
