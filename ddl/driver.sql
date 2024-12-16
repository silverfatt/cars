CREATE TABLE public.driver (
    id serial PRIMARY KEY,               
    name varchar NOT NULL,                        
    experience_years int2 NOT NULL,   
	car_id int4 NOT NULL,       
	violations INT DEFAULT 0,
    CONSTRAINT fk_car FOREIGN KEY (car_id) REFERENCES public.car (id) ON DELETE CASCADE
);
