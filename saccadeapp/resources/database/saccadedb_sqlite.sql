--===============================================
-- SQLite Script generated manually 
-- Date		: 18/05/2018
-- model	: saccadedb
-- author	: Christian Wiche
--===============================================
pragma recursive_triggers=1;
pragma foreign_keys=1;

---------------------------------------
---------------------------------------
create table if not exists configuration (
  	con_name    		varchar(50) 	not null	default 'Unnamed',
	con_tracker 		varchar(20)		not null	default 'eyegaze',
	con_monitor 		varchar(50)		not null	default 'default',
	con_screen  		int				not null 	default 0,
	con_path    		varchar(200)	not null	default './events',
	constraint con_pk primary key (con_name),
    constraint con_ak unique(con_name)
);
-- index
create index if not exists con_idx on configuration (con_name);

---------------------------------------
---------------------------------------
create table if not exists experiment (
	exp_code    		varchar(10)		not null    default '1234',
	exp_name    		varchar(50)	    not null    default 'Unnamed',
	exp_version    		varchar(10)		not null    default '1.0',
	exp_description 	text		    null        default '',
	exp_instructions    text		    null        default '',
	exp_comments    	text		    null        default '',
	exp_date_creation  	timestamp 		null		default current_timestamp,
	exp_date_update    	timestamp 		null		default current_timestamp,
	constraint exp_pk primary key (exp_name, exp_version),
    constraint exp_ak unique(exp_code)
);
-- date update
create trigger if not exists trg_exp
	after update of exp_code, exp_name, exp_version, exp_description, exp_instructions, exp_comments
	on experiment
	begin
		update experiment
		set exp_date_update = current_timestamp
		where exp_code = new.exp_code;
	end;
-- index
create index if not exists exp_idx on experiment (exp_code);

---------------------------------------
---------------------------------------
create table if not exists exp_dia (
	exp_code            varchar(10)		not null,
	dia_is_active       tinyint 		not null 	default 1,
	dia_ask_age         tinyint 		not null 	default 1,
	dia_ask_gender      tinyint 		not null 	default 1,
	dia_ask_glasses     tinyint 		not null 	default 1,
	dia_ask_eye_color   tinyint 		not null 	default 1,
	constraint exp_dia_pk primary key (exp_code),
	constraint exp_dia_fk
		foreign key (exp_code) references experiment (exp_code)
		on delete cascade
		on update cascade
);
-- index
create index if not exists exp_dia_idx on exp_dia (exp_code asc);

---------------------------------------
---------------------------------------
create table if not exists exp_con (
	exp_code            varchar(10)		not null,
	con_need_space      tinyint 		not null 	default 0,
	con_is_random       tinyint 		not null 	default 0,
	con_is_rest         tinyint 		not null 	default 0,
	con_rest_period     int 			not null	default 0,
	con_rest_time       float			not null	default 0.0,
	constraint exp_con_pk primary key (exp_code),
	constraint exp_con_fk
		foreign key (exp_code) references experiment (exp_code)
		on delete cascade
		on update cascade
);
-- index
create index if not exists exp_con_idx on exp_con (exp_code asc);

---------------------------------------
---------------------------------------
create table if not exists test (
	exp_code            varchar(10)     not null,
	tes_index	        int 		    not null,
	tes_name 	        varchar(50)     not null    default 'Unnamed',
	tes_description     text            null        default '',
	constraint tes_pk primary key (exp_code, tes_index),
    constraint tes_ak unique(exp_code, tes_name),
    constraint tes_fk
        foreign key (exp_code) references experiment (exp_code)
        on delete cascade
        on update cascade
);
-- index
create index if not exists tes_idx on test (exp_code asc, tes_index asc);

---------------------------------------
---------------------------------------
create table if not exists exp_seq (
    exp_code            varchar(10)     not null,
    tes_index           int             not null,
    seq_index           int             not null,
    tes_quantity        int             not null    default 1,
    constraint exp_seq_pk primary key (exp_code, tes_index, seq_index),
    constraint exp_seq_fk
        foreign key (exp_code, tes_index) references test (exp_code, tes_index)
        on delete cascade
        on update cascade
);
-- index
create index if not exists idx_exp_seq on exp_seq(exp_code asc, tes_index asc, seq_index asc);

---------------------------------------
---------------------------------------
create table if not exists frame (
    exp_code            varchar(10)     not null,
    tes_index           int	            not null,
	fra_index           int	            not null,
	fra_name            varchar(50)     not null    default 'Unnamed',
    fra_color           varchar(20)     not null    default 'black',
	fra_is_task         tinyint	        not null    default 0,
    fra_keys_allowed    text,
	fra_keys_selected   text,
    fra_time    float           not null    default 0.0,
	constraint fra_pk primary key (exp_code, tes_index, fra_index),
    constraint fra_ak unique (exp_code, tes_index, fra_name),
	constraint fra_fk
        foreign key (exp_code, tes_index) references test (exp_code, tes_index)
        on delete cascade
        on update cascade
);
-- index
create index if not exists fra_idx on frame (exp_code asc, tes_index asc, fra_index asc);

---------------------------------------
---------------------------------------
create table if not exists component (
	exp_code            varchar(10) 	not null,
  	tes_index           int				not null,
	fra_index           int				not null,
	com_index           int 			not null,
	com_name            varchar(50)     not null    default 'Unnamed',
	com_units           varchar(10)		not null 	default 'deg',
	com_pos_x           float 			not null 	default 0.0,
	com_pos_y           float 			not null 	default 0.0,
	com_rotation     	float 			not null 	default 0.0,
	com_size            float 			not null 	default 1.0,
    com_shape	        varchar(20)		not null 	default 'square',
	com_color	        varchar(20)		not null 	default 'white',
    com_image	        blob 			null,
	constraint com_pk primary key (exp_code, tes_index, fra_index, com_index),
    constraint com_ak unique(exp_code, tes_index, fra_index, com_name),
	constraint com_fk
		foreign key (exp_code, tes_index, fra_index) references frame (exp_code, tes_index, fra_index)
		on delete cascade
		on update cascade
);
-- index
create index if not exists com_idx on component (exp_code asc, tes_index asc, fra_index asc, com_index asc);
