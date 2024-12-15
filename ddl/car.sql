CREATE TABLE public.car (
	model varchar NOT NULL,
	year_of_manufacture int2 NOT NULL,
	mileage int4 NOT NULL,
	last_maintenance_date date NOT NULL,
	recommended_maintenance_date date NULL,
	id serial4 NOT NULL,
	CONSTRAINT car_pk PRIMARY KEY (id)
);
