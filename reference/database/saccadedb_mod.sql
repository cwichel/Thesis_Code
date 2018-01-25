-------------------------------------------------
-- Database basic configuration -----------------
-------------------------------------------------
pragma foreign_keys=1;
pragma recursive_triggers=1;

-------------------------------------------------
-- Master table cration -------------------------
-------------------------------------------------
create table if not exists master (
	mas_title			varchar(100) not null,
	mas_monitorid		int not null,
	mas_monitor_cfg		varchar(50) not null,
	mas_trackerid		int not null,
	mas_savepath		varchar(200) not null,
	primary key (mas_title)
);

-------------------------------------------------
-- Test table creation --------------------------
-------------------------------------------------
create table if not exists test (
	tes_code 			varchar(10) not null,
	tes_title 			varchar(100) not null,
	tes_version			varchar(10) not null,
	tes_description		mediumtext null,
	tes_datecreation 	timestamp null			default current_timestamp,
	tes_dateupdate 		timestamp null			default current_timestamp,
	primary key (
		tes_code, 
		tes_title, 
		tes_version
	)
);

-- trigger to auto-update date
create trigger if not exists trg_tes_dateupdate 
	after update of tes_code, tes_title, tes_version, tes_description 
	on test
begin
	update test 
	set tes_dateupdate=current_timestamp 
	where tes_code=new.tes_code;
end;

-------------------------------------------------
-- Experiment table creation --------------------
-------------------------------------------------
create table if not exists experiment (
	exp_code			varchar(10) not null,
	exp_title			varchar(100) not null,
	exp_version			varchar(10) not null,
	exp_description		mediumtext null,
	exp_comment			mediumtext null,
	exp_datecreation	timestamp null 			default current_timestamp,
	exp_dateupdate		timestamp null 			default current_timestamp,
	primary key (
		exp_code,
		exp_title,
		exp_version
	)
);

-- trigger to auto-update date
create trigger if not exists trg_exp_dateupdate
	after update of exp_code, exp_title, exp_version, exp_description, exp_comment
	on experiment
begin
	update experiment
	set exp_dateupdate=current_timestamp
	where exp_code = new.exp_code;
end;

-------------------------------------------------
-- exp_dialog table creation --------------------
-------------------------------------------------
create table if not exists exp_dialog (
	exp_code			varchar(10) not null,
	dia_enable			tinyint not null 		default 1,
	dia_askage 			tinyint not null 		default 1,
	dia_askgender 		tinyint not null 		default 1,
	dia_askglasses 		tinyint not null 		default 1,
	dia_askeyecolor 	tinyint not null 		default 1,
	primary key (exp_code)
	constraint fk_exp_dia
		foreign key (exp_code)
		references experiment (exp_code)
		on delete cascade 
		on update cascade
);

-------------------------------------------------
-- exp_config table creation --------------------
-------------------------------------------------
create table if not exists exp_config (
	exp_code			varchar(10) not null,
	con_spacepress		tinyint not null 		default 0,
	con_israndom		tinyint not null 		default 0,
	con_isrest			tinyint not null 		default 0,
	con_restperiod		int not null 			default 0,
	con_resttime		float not null 			default 0.0,
	primary key (exp_code)
	constraint fk_exp_con
		foreign key (exp_code)
		references experiment (exp_code)
		on delete cascade 
		on update cascade
);

-------------------------------------------------
-- exp_tes table creation -----------------------
-------------------------------------------------
create table if not exists exp_tes (
	tes_code 			varchar(10) not null,
	exp_code 			varchar(10) not null,
	exp_tes_id 			int not null 			default 1, 
	exp_tes_quantity 	int not null 			default 1,
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

-- index to accelerate search
create index if not exists idx_tes_exp on exp_tes (tes_code asc);
create index if not exists idx_exp_tes on exp_tes (exp_code asc);

-------------------------------------------------
-- tes_frame table creation ---------------------
-------------------------------------------------
create table if not exists tes_frame (
	tes_code 			varchar(10) not null,
	fra_id 				int not null 			default 1,
	fra_color			varchar(20) not null 	default 'black',
	fra_istask 			tinyint not null 		default 0,
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

-- index to accelerate search
create index if not exists idx_tes_fra on tes_frame (tes_code asc);

-------------------------------------------------
-- tes_fra_time table creation ------------------
-------------------------------------------------
create table if not exists tes_fra_time ( 
	tes_code 			varchar(10) not null,
	fra_id 				int not null 			default 1,
	tim_time 			float not null 			default 0.0,
	primary key (
		tes_code,
		fra_id
	)
	constraint fk_tes_fra_tim
		foreign key (tes_code, fra_id)
		references tes_frame (tes_code, fra_id)
		on delete cascade
		on update cascade
);

-------------------------------------------------
-- tes_fra_task table creation ------------------
-------------------------------------------------
create table if not exists tes_fra_task ( 
	tes_code 			varchar(10) not null,
	fra_id 				int not null 			default 1,
	tas_keysall 		text not null,
	tas_keyssel			text not null,
	primary key (
		tes_code,
		fra_id
	)
	constraint fk_tes_fra_tas
		foreign key (tes_code, fra_id)
		references tes_frame (tes_code, fra_id)
		on delete cascade
		on update cascade
);

-------------------------------------------------
-- tes_fra_object table creation ----------------
-------------------------------------------------
create table if not exists tes_fra_object (
	tes_code 			varchar(10) not null,
	fra_id 				int not null 			default 1,
	obj_id 				int not null 			default 1,
	obj_name 			varchar(50) not null,
	obj_units			varchar(10) not null 	default 'deg',
	obj_posx			float not null 			default 0.0,
	obj_posy			float not null 			default 0.0,
	obj_ori				float not null 			default 0.0,
	obj_isimg			tinyint not null 		default 0,
	obj_image			blob null,
	obj_shape 			varchar(20) not null 	default 'square',
	obj_color			varchar(20)	not null 	default 'white',
	primary key (
		tes_code,
		fra_id,
		obj_id
	)
	constraint fk_tes_fra_obj
		foreign key (tes_code, fra_id)
		references tes_frame (tes_code, fra_id)
		on delete cascade
		on update cascade
);

create index if not exists idx_tes_fra_obj on tes_fra_object (tes_code asc, fra_id asc);
