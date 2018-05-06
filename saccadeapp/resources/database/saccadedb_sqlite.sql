--===============================================
-- SQLite Script generated manually 
-- Date		: 29/01/2018
-- model	: saccadedb
-- author	: Christian Wiche
--===============================================
pragma recursive_triggers=1;
pragma foreign_keys=1;


--===============================================
-- MAIN CONFIG TABLE
--===============================================
create table if not exists master (
  	mas_name    		varchar(50) 	not null,
	mas_screen  		int				not null 	default 0,
	mas_tracker 		varchar(20)		not null	default 'None',
	mas_monitor 		varchar(50)		not null	default 'default',
	mas_path    		varchar(200)	not null	default './events',
	primary key (mas_name)
);

--===============================================
-- EXPERIMENT-RELATED TABLES
--===============================================
-- Experiment: base table -----------------------
create table if not exists experiment (
	exp_code    		varchar(10)		not null,
	exp_name    		varchar(50)	    not null,
	exp_version    		varchar(10)		not null,
	exp_description 	text		    null        default '',
	exp_instructions    text		    null        default '',
	exp_comments    	text		    null        default '',
	exp_date_creation  	timestamp 		null		default current_timestamp,
	exp_date_update    	timestamp 		null		default current_timestamp,
	primary key (
		exp_name,
		exp_version
	)
);
-- date update
create trigger if not exists trg_exp
	after update of
		exp_code,
		exp_name,
		exp_version,
		exp_description,
        exp_instructions,
		exp_comments
	on experiment
	begin
		update experiment
		set exp_date_update = current_timestamp
		where exp_code = new.exp_code;
	end;
-- index
create unique index if not exists unq_exp on experiment (exp_code);

-------------------------------------------------
-- Experiment: exp_dia --------------------------
create table if not exists exp_dia (
	exp_code            varchar(10)		not null,
	dia_is_active       tinyint 		not null 	default 1,
	dia_ask_age         tinyint 		not null 	default 1,
	dia_ask_gender      tinyint 		not null 	default 1,
	dia_ask_glasses     tinyint 		not null 	default 1,
	dia_ask_eye_color   tinyint 		not null 	default 1,
	primary key (exp_code)
	constraint fk_exp_dia
		foreign key (exp_code)
		references experiment (exp_code)
		on delete cascade
		on update cascade
);
-- index
create index if not exists idx_exp_dia on exp_dia (exp_code asc);

-------------------------------------------------
-- Experiment: exp_con --------------------------
create table if not exists exp_con (
	exp_code            varchar(10)		not null,
	con_need_space      tinyint 		not null 	default 0,
	con_is_random       tinyint 		not null 	default 0,
	con_is_rest         tinyint 		not null 	default 0,
	con_rest_period     int 			not null	default 0,
	con_rest_time       float			not null	default 0.0,
	primary key (exp_code)
	constraint fk_exp_con
		foreign key (exp_code)
		references experiment (exp_code)
		on delete cascade
		on update cascade
);
-- index
create index if not exists idx_exp_con on exp_con (exp_code asc);

--===============================================
-- TEST-RELATED TABLES (EXPERIMENT CHILD)
--===============================================
-- Test: base table -----------------------------
create table if not exists test (
	exp_code            varchar(10)     not null,
	tes_index	        int 		    not null    default 1,
	tes_name 	        varchar(50)     not null    default 'Unnamed',
	tes_description     text            null        default '',
    tes_quantity        int             not null    default 1,
	primary key (
		exp_code,
        tes_index
	)
    constraint fk_tes
        foreign key (exp_code)
        references experiment (exp_code)
        on delete cascade
        on update cascade
);
-- index
create index if not exists idx_tes on test (exp_code asc, tes_index asc);

-------------------------------------------------
-- Test: tes_frame ------------------------------
create table if not exists frame (
    exp_code            varchar(10)     not null,
    tes_index           int	            not null    default 1,
	fra_index           int	            not null    default 1,
	fra_name            varchar(50)     not null    default 'Unnamed',
    fra_color           varchar(20)     not null    default 'black',
	fra_is_task         tinyint	        not null    default 0,
    fra_keys_allowed    text,
	fra_keys_selected   text,
    fra_time    float           not null    default 0.0,
	primary key (
		exp_code,
        tes_index,
		fra_index
	)
	constraint fk_fra
        foreign key (exp_code, tes_index)
        references test (exp_code, tes_index)
        on delete cascade
        on update cascade
);
-- index
create index if not exists idx_fra on frame (exp_code asc, tes_index asc, fra_index asc);

-- Test: tes_fra_object -------------------------
create table if not exists component (
	exp_code            varchar(10) 	not null,
  	tes_index           int				not null	default 1,
	fra_index           int				not null	default 1,
	com_index           int 			not null	default 1,
	com_name            varchar(50)     not null    default 'Unnamed',
	com_units           varchar(10)		not null 	default 'deg',
	com_pos_x           float 			not null 	default 0.0,
	com_pos_y           float 			not null 	default 0.0,
	com_orientation     float 			not null 	default 0.0,
	com_size            float 			not null 	default 1.0,
    com_shape	        varchar(20)		not null 	default 'square',
	com_image	        blob 			null,
	com_color	        varchar(20)		not null 	default 'white',
	primary key (
		exp_code,
        tes_index,
		fra_index,
        com_index
	)
	constraint fk_obj
		foreign key (exp_code, tes_index, fra_index)
		references frame (exp_code, tes_index, fra_index)
		on delete cascade
		on update cascade
);
-- index
create index if not exists idx_obj on component (exp_code asc, tes_index asc, fra_index asc, com_index asc);
