CREATE SEQUENCE public.categories_id_seq
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START 1
    CACHE 1;

CREATE TABLE public.categories(
    id integer NOT NULL DEFAULT nextval('categories_id_seq'::regclass),
    name character varying NOT NULL,
    description character varying,
    definition character varying,
    CONSTRAINT categories_pkey PRIMARY KEY (id),
    CONSTRAINT categories_definition_fkey FOREIGN KEY (definition)
        REFERENCES public.observed_properties (def) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);
