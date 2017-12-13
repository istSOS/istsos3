CREATE EXTENSION postgis;

CREATE SCHEMA data;

CREATE SEQUENCE data.observations_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1000;

CREATE SEQUENCE observed_properties_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

CREATE TABLE public.observed_properties
(
   id integer NOT NULL default nextval('observed_properties_id_seq'),
   name character varying,
   def character varying NOT NULL,
   description character varying,
   PRIMARY KEY (id),
   UNIQUE (name),
   UNIQUE (def)
);

INSERT INTO public.observed_properties VALUES
(1, 'air-temperature',
    'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature',
    'Air temperature at 2 meters above terrain'),
(2, 'air-rainfall',
    'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:rainfall',
    'Liquid precipitation or snow water equivalent'),
(3, 'air-relative-humidity',
    'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:humidity:relative',
    'Absolute humidity relative to the maximum for that air'),
(4, 'air-wind-velocity',
    'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:wind:velocity',
    'Wind speed at 1 meter above terrain'),
(5, 'solar-radiation',
    'urn:ogc:def:parameter:x-istsos:1.0:meteo:solar:radiation',
    'Direct radiation sum in spectrum rand'),
(6, 'river-height',
    'urn:ogc:def:parameter:x-istsos:1.0:river:water:height',
    ''),
(7, 'river-discharge',
    'urn:ogc:def:parameter:x-istsos:1.0:river:water:discharge',
    ''),
(8, 'soil-evapotranspiration',
    'urn:ogc:def:parameter:x-istsos:1.0:meteo:soil:evapotranspiration',
    ''),
(9, 'air-heatindex',
    'urn:ogc:def:parameter:x-istsos:1.0:meteo:air:heatindex',
    '');
SELECT pg_catalog.setval('observed_properties_id_seq', 9, true);

CREATE SEQUENCE uoms_id_uom_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

CREATE TABLE public.uoms
(
    id integer NOT NULL default nextval('uoms_id_uom_seq'),
    name character varying NOT NULL,
    description character varying,
    PRIMARY KEY (id),
    UNIQUE (name)
);

INSERT INTO uoms VALUES
    (0, 'null', ''),
    (1, 'mm', 'millimeter'),
    (2, '°C', 'Celsius degree'),
    (3, '%', 'percentage'),
    (4, 'm/s', 'metre per second'),
    (5, 'W/m2', 'Watt per square metre'),
    (6, '°F', 'Fahrenheit degree'),
    (7, 'm', 'metre'),
    (8, 'm3/s', 'cube meter per second'),
    (9, 'mm/h', 'evapotranspiration'),
    (10, 'g', 'gram'),
    (11, 'Kg', 'kilogram'),
    (12, 'ml', 'milliliter'),
    (13, 'l', 'liter');

SELECT pg_catalog.setval('uoms_id_uom_seq', 9, true);

CREATE SEQUENCE material_classes_id_mcl_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

CREATE TABLE public.material_classes
(
    id integer NOT NULL default nextval('material_classes_id_mcl_seq'),
    name character varying NOT NULL,
    definition character varying NOT NULL,
    description character varying,
    image character varying,
    PRIMARY KEY (id),
    UNIQUE (definition)
);

INSERT INTO material_classes VALUES
    (1,
        'soil',
        'http://www.opengis.net/def/material/OGC-OM/2.0/soil',
        '',
        '/img/materials/soil.png'),
    (2,
        'water',
        'http://www.opengis.net/def/material/OGC-OM/2.0/water',
        '',
        '/img/materials/water.png'),
    (3,
        'rock',
        'http://www.opengis.net/def/material/OGC-OM/2.0/rock',
        '',
        '/img/materials/rock.png'),
    (4,
        'tissue',
        'http://www.opengis.net/def/material/OGC-OM/2.0/tissue',
        '',
        '/img/materials/tissue.png'
    );

SELECT pg_catalog.setval('material_classes_id_mcl_seq', 4, true);


CREATE SEQUENCE methods_id_met_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

CREATE TABLE public.methods
(
    id integer NOT NULL default nextval('methods_id_met_seq'),
    identifier character varying NOT NULL,
    name character varying NOT NULL,
    description character varying,
    PRIMARY KEY (id),
    UNIQUE (identifier)
);

-- Sampling method techniques:
-- http://www.who.int/water_sanitation_health/dwq/2edvol3d.pdf
-- http://www.umich.edu/~chemstu/assignments/Scholarship/water%20sampling.pdf
-- https://water.usgs.gov/owq/FieldManual/chapter4/pdf/Chap4_v2.pdf
INSERT INTO methods VALUES
    (1,
        '/filtration/membrane',
        'membrane filtration',
        ''),
    (2,
        '/equal/width/increment',
        'equal width increment - EWI',
        ''),
    (3,
        '/equal/discharge/increment',
        'equal discharge increment - EDI',
        '');

SELECT pg_catalog.setval('methods_id_met_seq', 3, true);

CREATE SEQUENCE offerings_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 10;

CREATE TABLE public.offerings
(
    id integer NOT NULL default nextval('offerings_id_seq'),
    data_table_exists boolean DEFAULT FALSE,
    offering_name character varying NOT NULL,
    procedure_name character varying NOT NULL,
    description_format character varying,
    foi_type character varying NOT NULL,
    sampled_foi character varying,
    fixed boolean DEFAULT FALSE,
    pt_begin timestamp with time zone,
    pt_end timestamp with time zone,
    rt_begin timestamp with time zone,
    rt_end timestamp with time zone,
    observed_area geometry,
    cached jsonb,
    config jsonb,
    PRIMARY KEY (id),
    UNIQUE (offering_name),
    UNIQUE (procedure_name)
);

CREATE INDEX
   ON public.offerings USING btree (id ASC NULLS LAST);

CREATE SEQUENCE sensor_descriptions_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

CREATE TABLE public.sensor_descriptions
(
    id integer NOT NULL default nextval('sensor_descriptions_id_seq'),
    id_off integer NOT NULL,
    valid_time_begin timestamp with time zone,
    valid_time_end timestamp with time zone,
    data character varying,
    short_name character varying,
    keywords character varying[],
    description character varying,
    manufacturer character varying,
    model_number character varying,
    serial_number character varying,
    sampling_resolution interval,
    acquisition_resolution interval,
    storage_capacity character varying,
    battery_capacity character varying,
    owner character varying,
    operator character varying,
    PRIMARY KEY (id),
    FOREIGN KEY (id_off) REFERENCES offerings (id)
        ON UPDATE NO ACTION ON DELETE CASCADE
);

CREATE INDEX
   ON public.sensor_descriptions USING btree (id_off ASC NULLS LAST);

CREATE SEQUENCE off_obs_prop_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

CREATE TABLE public.off_obs_prop
(
    id integer NOT NULL default nextval('off_obs_prop_id_seq'),
    id_off integer NOT NULL,
    id_opr integer NOT NULL,
    id_uom integer,
    observation_type character varying,
    col_name character varying,
    PRIMARY KEY (id),
    FOREIGN KEY (id_off) REFERENCES offerings (id)
        ON UPDATE NO ACTION ON DELETE CASCADE,
    FOREIGN KEY (id_opr) REFERENCES observed_properties (id)
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY (id_uom) REFERENCES uoms (id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE INDEX
   ON public.off_obs_prop USING btree (id_off ASC NULLS LAST);

CREATE SEQUENCE off_obs_type_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

CREATE TABLE public.off_obs_type
(
    id integer NOT NULL default nextval('off_obs_type_id_seq'),
    id_off integer NOT NULL,
    observation_type character varying,
    PRIMARY KEY (id),
    FOREIGN KEY (id_off) REFERENCES offerings (id)
        ON UPDATE NO ACTION ON DELETE CASCADE
);

CREATE INDEX
   ON public.off_obs_type USING btree (id_off ASC NULLS LAST);

CREATE TABLE public.fois
(
   id serial NOT NULL,
   description character varying,
   identifier character varying NOT NULL,
   foi_name character varying,
   foi_type character varying,
   geom geometry,
   PRIMARY KEY (id),
   UNIQUE (identifier)
);

CREATE TABLE public.sampled_foi
(
    id integer NOT NULL,
    id_sam integer NOT NULL,
    PRIMARY KEY (id, id_sam),
    FOREIGN KEY (id) REFERENCES public.fois (id)
        ON UPDATE NO ACTION ON DELETE CASCADE,
    FOREIGN KEY (id_sam) REFERENCES public.fois (id)
        ON UPDATE NO ACTION ON DELETE CASCADE
);

CREATE SEQUENCE specimen_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


CREATE TABLE public.specimens
(
    id integer NOT NULL DEFAULT nextval('specimen_id_seq'),
    offering_name character varying NOT NULL,
    foi_name character varying NOT NULL,
    description character varying,
    identifier character varying NOT NULL,
    sampled_feature character varying,
    material character varying,
    sampling_time timestamp with time zone NOT NULL,
    method character varying,
    --sampling_location geometry,
    sampling_size double precision,
    sampling_uom character varying,
    current_location character varying,
    speciment_type character varying,

    PRIMARY KEY (id),
    UNIQUE (identifier),

    CONSTRAINT specimen_offering_name_fkey FOREIGN KEY (offering_name)
      REFERENCES offerings (offering_name) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,

    CONSTRAINT specimen_sampled_feature_fkey FOREIGN KEY (sampled_feature)
      REFERENCES fois (identifier) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,

    CONSTRAINT specimen_material_fkey FOREIGN KEY (material)
      REFERENCES material_classes (definition) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,

    CONSTRAINT specimen_method_fkey FOREIGN KEY (method)
      REFERENCES methods (identifier) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,

    CONSTRAINT specimen_sampling_uom_fkey FOREIGN KEY (sampling_uom)
      REFERENCES uoms (name) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE SEQUENCE processing_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

CREATE TABLE public.processing
(
    id integer NOT NULL DEFAULT nextval('processing_id_seq'),
    id_spec integer,
    process_operator character varying NOT NULL,
    processing_details character varying NOT NULL,
    processing_time timestamp with time zone,
    PRIMARY KEY (id),

    CONSTRAINT specimen_id_spec_fkey FOREIGN KEY (id_spec)
      REFERENCES specimens (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
);

INSERT INTO public.fois(
    description, identifier, foi_name, foi_type, geom)
VALUES (
    'There is no value',
    'http://www.opengis.net/def/nil/OGC/0/inapplicable',
    'Inapplicable', NULL, NULL
),(
    'The correct value is not readily available to the sender of this data. Furthermore, a correct value may not exist',
    'http://www.opengis.net/def/nil/OGC/0/missing',
    'Missing', NULL, NULL
),(
    'The correct value is not known to, or not computable by, the sender of this data. However, the correct value probably exists',
    'http://www.opengis.net/def/nil/OGC/0/unknown',
    'Unknown', NULL, NULL
);


CREATE TABLE public.humans(
    id serial,
    username character varying NOT NULL,
    pword character varying NOT NULL,
    firstname character varying,
    middlename character varying,
    lastname character varying,
    organisation_name character varying,
    position_name character varying,
    role_name character varying,
    telephone character varying,
    fax character varying,
    email character varying,
    web character varying,
    address character varying,
    city character varying,
    adminarea character varying,
    postalcode character varying,
    country character varying,
    PRIMARY KEY (id),
    UNIQUE (username)
);


CREATE SEQUENCE processing_details_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

CREATE TABLE public.processing_details
(
   id integer NOT NULL default nextval('processing_details_id_seq'),
   name character varying,
   identifier character varying NOT NULL,
   description character varying,
   PRIMARY KEY (id),
   UNIQUE (name),
   UNIQUE (identifier)
);
