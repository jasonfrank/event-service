create table if not exists event (
  	id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  	application_id INT NOT NULL,
	event_time BIGINT NOT NULL,
	event_type_id INT NOT NULL,
	headline varchar(200) NOT NULL,
	body varchar(4192),
	index idx_time(event_time),
	index idx_type_time(application_id, event_type_id, event_time),
	primary key (id)
) Engine=InnoDB;

create table if not exists event_entity (
  	id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	event_id BIGINT UNSIGNED NOT NULL,
	entity_type INT NOT NULL,
	entity_id BIGINT NOT NULL,
	UNIQUE idx_ee(event_id, entity_type, entity_id),
	INDEX idx_entity(entity_id),
	primary key (id)
) Engine=InnoDB;
