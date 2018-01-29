--===============================================
-- SQLite Script generated manually 
-- Date		: 24/01/2018
-- model	: saccadedb
-- version	: 1.0
-- author	: Christian Wiche
--===============================================
pragma recursive_triggers=1;
pragma foreign_keys=1;


--===============================================
-- MAIN CONFIG TABLE
--===============================================
create table if not exists master (
  	mas_title			varchar(100) 	not null,
	mas_screen			int				not null 	default 0,
	mas_tracker			int				not null	default 0,
	mas_monitor			varchar(50)		not null	default 'default',
	mas_save_path		varchar(200)	not null	default './events',
	primary key (mas_title)
);


--===============================================
-- TEST-RELATED TABLES
--===============================================
-- Test: base table -----------------------------
create table if not exists test (
	tes_code			varchar(10) 	not null,
	tes_title 			varchar(100) 	not null,
	tes_version 		varchar(10)		not null,
	tes_description 	mediumtext 		null,
	tes_date_create 	timestamp		null 		default current_timestamp,
	tes_date_update		timestamp 		null 		default current_timestamp,
	primary key (
		tes_title,
		tes_version
	)
);

-- Test unique index
create unique index if not exists unq_tes_cod on test (tes_code);
-- Test trigger
create trigger if not exists trg_tes_dat
	after update of
		tes_code,
		tes_title,
		tes_version,
		tes_description
	on test
	begin
		update test
		set tes_date_update = current_timestamp
		where tes_code = new.tes_code;
	end;

-- Test: tes_frame ------------------------------
create table if not exists tes_frame (
	tes_code			varchar(10) 	not null,
	fra_id				int				not null	default 1,
	fra_color			varchar(20)		not null	default 'black',
	fra_is_task			tinyint			not null	default 0,
	primary key (
		tes_code,
		fra_id
	)
	constraint fk_tes_fra
		foreign key (tes_code)
		references test (tes_code)
		on delete cascade
		on update cascade
);

-- tes_frame index
create index if not exists idx_tes_fra on tes_frame (tes_code asc);

-- Test: tes_fra_time ---------------------------
create table if not exists tes_fra_time (
	tes_code			varchar(10) 	not null,
	fra_id				int				not null	default 1,
	tim_time 			float			not null 	default 0.0,
	primary key (
		tes_code,
		fra_id
	)
	constraint fk_tes_fra_tim
		foreign key (
			tes_code,
			fra_id
		)
		references tes_frame (
			tes_code,
			fra_id
		)
		on delete cascade
		on update cascade
);

-- Test: tes_fra_task ---------------------------
create table if not exists tes_fra_task (
	tes_code			varchar(10)		not null,
	fra_id				int				not null	default 1,
	tas_key_all 		text			not null,
	tas_key_sel			text			not null,
	primary key (
		tes_code,
		fra_id
	)
	constraint fk_tes_fra_tas
		foreign key (
			tes_code,
			fra_id
		)
		references tes_frame (
			tes_code,
			fra_id
		)
		on delete cascade
		on update cascade
);

-- Test: tes_fra_object -------------------------
create table if not exists tes_fra_object (
	tes_code			varchar(10) 	not null,
	fra_id				int				not null	default 1,
	obj_id 				int 			not null	default 1,
	obj_name			varchar(50)		null,
	obj_units			varchar(10)		not null 	default 'degFlat',
	obj_posx			float 			not null 	default 0.0,
	obj_posy			float 			not null 	default 0.0,
	obj_ori				float 			not null 	default 0.0,
	obj_size 			float 			not null 	default 1.0,
	obj_is_img			tinyint 		not null 	default 0,
	obj_image			blob 			null,
	obj_shape			varchar(20)		not null 	default 'square',
	obj_color			varchar(20)		not null 	default 'white',
	primary key (
		tes_code,
		fra_id,
		obj_id
	)
	constraint fk_tes_fra_obj
		foreign key (
			tes_code,
			fra_id
		)
		references tes_frame (
			tes_code,
			fra_id
		)
		on delete cascade
		on update cascade
);

-- tes_fra_obj index
create index if not exists idx_tes_fra_obj on tes_fra_object (tes_code asc, fra_id asc);


--===============================================
-- EXPERIMENT-RELATED TABLES
--===============================================
-- Experiment: base table -----------------------
create table if not exists experiment (
	exp_code			varchar(10)		not null,
	exp_title			varchar(100)	not null,
	exp_version			varchar(10)		not null,
	exp_description		mediumtext		null,
	exp_comment			mediumtext		null,
	exp_date_create		timestamp 		null		default current_timestamp,
	exp_date_update		timestamp 		null		default current_timestamp,
	primary key (
		exp_title,
		exp_version
	)
);

-- Test unique index
create unique index if not exists unq_exp_cod on experiment (exp_code);
-- Experiment trigger
create trigger if not exists trg_exp_dat
	after update of
		exp_code,
		exp_title,
		exp_version,
		exp_description,
		exp_comment
	on experiment
	begin
		update experiment
		set exp_date_update = current_timestamp
		where exp_code = new.exp_code;
	end;

-- Experiment: exp_dia --------------------------
create table if not exists exp_dia (
	exp_code			varchar(10)		not null,
	dia_enable			tinyint 		not null 	default 1,
	dia_ask_age			tinyint 		not null 	default 1,
	dia_ask_gender		tinyint 		not null 	default 1,
	dia_ask_glasses		tinyint 		not null 	default 1,
	dia_ask_eye_color	tinyint 		not null 	default 1,
	primary key (exp_code)
	constraint fk_exp_dia
		foreign key (exp_code)
		references experiment (exp_code)
		on delete cascade
		on update cascade
);

-- Experiment: exp_con --------------------------
create table if not exists exp_con (
	exp_code			varchar(10)		not null,
	con_space_start		tinyint 		not null 	default 0,
	con_is_rand			tinyint 		not null 	default 0,
	con_is_rest			tinyint 		not null 	default 0,
	con_rest_test		int 			not null	default 0,
	con_rest_time		float			not null	default 0.0,
	primary key (exp_code)
	constraint fk_exp_con
		foreign key (exp_code)
		references experiment (exp_code)
		on delete cascade
		on update cascade
);


--===============================================
-- EXPERIMENT-TEST RELATION TABLE
--===============================================
create table if not exists exp_tes (
	tes_code			varchar(10)		not null,
	exp_code			varchar(10)		not null,
	exp_tes_id			int 			not null	default 1,
	exp_tes_quantity	int 			not null 	default 1,
	primary key (
		tes_code,
		exp_code,
		exp_tes_id
	)
	constraint fk_tes_exp
		foreign key (tes_code)
		references test (tes_code)
		on delete restrict
		on update cascade
	constraint fk_exp_tes
		foreign key (exp_code)
		references experiment (exp_code)
		on delete cascade
		on update cascade
);

-- tes_fra_obj index
create index if not exists idx_tes_exp on exp_tes (tes_code asc);
create index if not exists idx_exp_tes on exp_tes (exp_code asc);

--===============================================
