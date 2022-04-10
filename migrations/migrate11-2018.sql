ALTER TABLE exam_concept_score RENAME TO cohort_exam_concept_score;
ALTER TABLE question_concept_score RENAME TO cohort_question_concept_score;

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
-- Name: user_exam_concept_score; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_exam_concept_score (
    user_key character varying(100) NOT NULL,
    exam_id integer NOT NULL,
    score double precision,
    concept_id integer NOT NULL
);


ALTER TABLE public.user_exam_concept_score OWNER TO postgres;

--
-- Name: user_exam_concept_score user_exam_concept_score_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_exam_concept_score
    ADD CONSTRAINT user_exam_concept_score_pkey PRIMARY KEY (user_key, exam_id, concept_id);


--
-- Name: user_exam_concept_score user_exam_concept_score_concept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_exam_concept_score
    ADD CONSTRAINT user_exam_concept_score_concept_id_fkey FOREIGN KEY (concept_id) REFERENCES public.concept(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_exam_concept_score user_exam_concept_score_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_exam_concept_score
    ADD CONSTRAINT user_exam_concept_score_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exam(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_exam_concept_score user_exam_concept_score_user_key_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_exam_concept_score
    ADD CONSTRAINT user_exam_concept_score_user_key_fkey FOREIGN KEY (user_key) REFERENCES public."user"(key) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: user_question_concept_score; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_question_concept_score (
    user_key character varying(100) NOT NULL,
    question_id integer NOT NULL,
    score double precision,
    concept_id integer NOT NULL
);


ALTER TABLE public.user_question_concept_score OWNER TO postgres;

--
-- Name: user_question_concept_score user_question_concept_score_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_question_concept_score
    ADD CONSTRAINT user_question_concept_score_pkey PRIMARY KEY (user_key, question_id, concept_id);


--
-- Name: user_question_concept_score user_question_concept_score_concept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_question_concept_score
    ADD CONSTRAINT user_question_concept_score_concept_id_fkey FOREIGN KEY (concept_id) REFERENCES public.concept(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_question_concept_score user_question_concept_score_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_question_concept_score
    ADD CONSTRAINT user_question_concept_score_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.question(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_question_concept_score user_question_concept_score_user_key_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_question_concept_score
    ADD CONSTRAINT user_question_concept_score_user_key_fkey FOREIGN KEY (user_key) REFERENCES public."user"(key) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

