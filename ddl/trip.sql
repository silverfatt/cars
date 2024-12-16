CREATE TABLE public.trip (
    id serial PRIMARY KEY,                 
    trip_date date NOT NULL,              
    distance_km float4 NOT NULL,           
    rating int2 CHECK (rating BETWEEN 1 AND 5),
    cost numeric(10, 2) NOT NULL, 
	driver_id int4 NOT NULL,         
    CONSTRAINT fk_driver FOREIGN KEY (driver_id) REFERENCES public.driver (id) ON DELETE CASCADE
);