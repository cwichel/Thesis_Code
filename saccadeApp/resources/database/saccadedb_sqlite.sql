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
  	mas_name    varchar(100) 	not null,
	mas_scrn    int				not null 	default 0,
	mas_trck    int				not null	default 0,
	mas_mont    varchar(50)		not null	default 'default',
	mas_path    varchar(200)	not null	default './events',
	primary key (mas_name)
);

--===============================================
-- EXPERIMENT-RELATED TABLES
--===============================================
-- Experiment: base table -----------------------
create table if not exists experiment (
	exp_code    varchar(10)		not null,
	exp_name    varchar(50)	    not null,
	exp_vers    varchar(10)		not null,
	exp_desc    text		    null,
	exp_comm    text		    null,
	exp_datc    timestamp 		null		default current_timestamp,
	exp_datu    timestamp 		null		default current_timestamp,
	primary key (
		exp_name,
		exp_vers
	)
);
-- date update
create trigger if not exists trg_exp
	after update of
		exp_code,
		exp_name,
		exp_vers,
		exp_desc,
		exp_comm
	on experiment
	begin
		update experiment
		set exp_datu = current_timestamp
		where exp_code = new.exp_code;
	end;
-- index
create unique index if not exists unq_exp on experiment (exp_code);

-------------------------------------------------
-- Experiment: exp_dia --------------------------
create table if not exists exp_dia (
	exp_code    varchar(10)		not null,
	dia_fact    tinyint 		not null 	default 1,
	dia_fage    tinyint 		not null 	default 1,
	dia_fgen    tinyint 		not null 	default 1,
	dia_fgla    tinyint 		not null 	default 1,
	dia_feye    tinyint 		not null 	default 1,
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
	exp_code    varchar(10)		not null,
	con_fspc    tinyint 		not null 	default 0,
	con_frnd    tinyint 		not null 	default 0,
	con_frst    tinyint 		not null 	default 0,
	con_reps    int 			not null	default 0,
	con_time    float			not null	default 0.0,
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
	exp_code    varchar(10)     not null,
	tes_indx	int 		    not null    default 1,
	tes_name 	varchar(50)     not null    default 'unnamed',
	tes_desc 	text            null,
    tes_reps    int             not null    default 1,
	primary key (
		exp_code,
        tes_indx
	)
    constraint fk_tes
        foreign key (exp_code)
        references experiment (exp_code)
        on delete cascade
        on update cascade
);
-- index
create index if not exists idx_tes on test (exp_code asc, tes_indx asc);

-------------------------------------------------
-- Test: tes_frame ------------------------------
create table if not exists frame (
    exp_code    varchar(10)     not null,
    tes_indx    int	            not null    default 1,
	fra_indx    int	            not null    default 1,
	fra_name    varchar(50)     not null    default 'unnamed',
    fra_colr    varchar(20)     not null    default 'black',
	fra_task    tinyint	        not null    default 0,
    fra_time    float           not null    default 0.0,
    fra_keya    text,
	fra_keys    text,
	primary key (
		exp_code,
        tes_indx,
		fra_indx
	)
	constraint fk_fra
        foreign key (exp_code, tes_indx)
        references test (exp_code, tes_indx)
        on delete cascade
        on update cascade
);
-- index
create index if not exists idx_fra on frame (exp_code asc, tes_indx asc, fra_indx asc);

-- Test: tes_fra_object -------------------------
create table if not exists component (
	exp_code    varchar(10) 	not null,
  	tes_indx    int				not null	default 1,
	fra_indx    int				not null	default 1,
	com_indx    int 			not null	default 1,
	com_name    varchar(50)     not null    default 'unnamed',
	com_unit    varchar(10)		not null 	default 'deg',
	com_posx    float 			not null 	default 0.0,
	com_posy    float 			not null 	default 0.0,
	com_orie    float 			not null 	default 0.0,
	com_size    float 			not null 	default 1.0,
	com_fimg	tinyint 		not null 	default 0,
	com_imag	blob 			null,
	com_shpe	varchar(20)		not null 	default 'square',
	com_colr	varchar(20)		not null 	default 'white',
	primary key (
		exp_code,
        tes_indx,
		fra_indx,
        com_indx
	)
	constraint fk_obj
		foreign key (exp_code, tes_indx, fra_indx)
		references frame (exp_code, tes_indx, fra_indx)
		on delete cascade
		on update cascade
);
-- index
create index if not exists idx_obj on component (exp_code asc, tes_indx asc, fra_indx asc, com_indx asc);
