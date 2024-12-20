CREATE TABLE public.users (
    id serial PRIMARY KEY,               
    hashed_password varchar NOT NULL,                        
    email varchar NOT NULL,   
	phone varchar NOT NULL,       
	initials varchar NOT NULL,
    position varchar NOT NULL
);