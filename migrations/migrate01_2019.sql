--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.10
-- Dumped by pg_dump version 10.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: study_material; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.study_material (
    date_added timestamp without time zone,
    last_updated timestamp without time zone,
    id integer NOT NULL,
    title character varying(100),
    link character varying(100),
    description character varying(200),
    material_type character varying(100)
);


ALTER TABLE public.study_material OWNER TO postgres;

--
-- Name: study_material_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.study_material_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.study_material_id_seq OWNER TO postgres;

--
-- Name: study_material_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.study_material_id_seq OWNED BY public.study_material.id;


--
-- Name: study_material id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.study_material ALTER COLUMN id SET DEFAULT nextval('public.study_material_id_seq'::regclass);


--
-- Name: study_material_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.study_material_id_seq', 1, true);


--
-- Name: study_material study_material_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.study_material
    ADD CONSTRAINT study_material_pkey PRIMARY KEY (id);


--
-- Name: concept_material_link; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.concept_material_link (
    id integer NOT NULL,
    concept_id integer,
    material_id integer
);


ALTER TABLE public.concept_material_link OWNER TO postgres;

--
-- Name: concept_material_link_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.concept_material_link_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.concept_material_link_id_seq OWNER TO postgres;

--
-- Name: concept_material_link_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.concept_material_link_id_seq OWNED BY public.concept_material_link.id;


--
-- Name: concept_material_link id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.concept_material_link ALTER COLUMN id SET DEFAULT nextval('public.concept_material_link_id_seq'::regclass);


--
-- Name: concept_material_link_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.concept_material_link_id_seq', 1, true);


--
-- Name: concept_material_link concept_material_link_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.concept_material_link
    ADD CONSTRAINT concept_material_link_pkey PRIMARY KEY (id);


--
-- Name: concept_material_link concept_material_link_concept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.concept_material_link
    ADD CONSTRAINT concept_material_link_concept_id_fkey FOREIGN KEY (concept_id) REFERENCES public.concept(id) ON DELETE CASCADE;


--
-- Name: concept_material_link concept_material_link_material_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.concept_material_link
    ADD CONSTRAINT concept_material_link_material_id_fkey FOREIGN KEY (material_id) REFERENCES public.study_material(id) ON DELETE CASCADE;


--
-- Name: user_settings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_settings (
    date_added timestamp without time zone,
    last_updated timestamp without time zone,
    id integer NOT NULL,
    user_id character varying,
    preferences character varying(200)
);


ALTER TABLE public.user_settings OWNER TO postgres;

--
-- Name: user_settings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_settings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_settings_id_seq OWNER TO postgres;

--
-- Name: user_settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_settings_id_seq OWNED BY public.user_settings.id;


--
-- Name: user_settings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_settings ALTER COLUMN id SET DEFAULT nextval('public.user_settings_id_seq'::regclass);


--
-- Name: user_settings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_settings_id_seq', 1, false);


--
-- Name: user_settings user_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_settings
    ADD CONSTRAINT user_settings_pkey PRIMARY KEY (id);


--
-- Name: user_settings user_settings_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_settings
    ADD CONSTRAINT user_settings_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(key);

--
-- PostgreSQL database dump complete
--

