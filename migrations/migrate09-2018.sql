ALTER TABLE answer
ADD COLUMN date_added timestamp,
ADD COLUMN last_updated timestamp;

CREATE TABLE public.cohort_concept_score (
    course_id integer NOT NULL,
    score double precision,
    concept_id integer NOT NULL
);

ALTER TABLE public.cohort_score OWNER TO postgres;


ALTER TABLE ONLY public.cohort_concept_score
    ADD CONSTRAINT cohort_concept_score_pkey PRIMARY KEY (course_id, concept_id);


--
-- Name: cohort_concept_score cohort_concept_score_concept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cohort_concept_score
    ADD CONSTRAINT cohort_concept_score_concept_id_fkey FOREIGN KEY (concept_id) REFERENCES public.concept(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: cohort_concept_score cohort_concept_score_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cohort_concept_score
    ADD CONSTRAINT cohort_concept_score_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.course(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE collection
ADD COLUMN date_added timestamp,
ADD COLUMN last_updated timestamp;

ALTER TABLE concept
ADD COLUMN date_added timestamp,
ADD COLUMN last_updated timestamp,
ADD COLUMN scores_last_updated timestamp;

ALTER TABLE concept_value
ADD COLUMN date_added timestamp,
ADD COLUMN last_updated timestamp;

ALTER TABLE connectorsettings
ADD COLUMN date_added timestamp,
ADD COLUMN last_updated timestamp;

ALTER TABLE course RENAME enddate TO end_date;
ALTER TABLE course RENAME startdate TO start_date;

ALTER TABLE course
ADD COLUMN date_added timestamp,
ADD COLUMN last_updated timestamp;

ALTER TABLE exam
DROP COLUMN date,
ADD COLUMN date_added timestamp,
ADD COLUMN last_updated timestamp,
ADD COLUMN start_time timestamp,
ADD COLUMN end_time timestamp;

CREATE TABLE public.exam_concept_score (
    exam_id integer NOT NULL,
    score double precision,
    concept_id integer NOT NULL
);

ALTER TABLE public.exam_concept_score OWNER TO postgres;

ALTER TABLE ONLY public.exam_concept_score
    ADD CONSTRAINT exam_concept_score_pkey PRIMARY KEY (exam_id, concept_id);


--
-- Name: exam_concept_score exam_concept_score_concept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_concept_score
    ADD CONSTRAINT exam_concept_score_concept_id_fkey FOREIGN KEY (concept_id) REFERENCES public.concept(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: exam_concept_score exam_concept_score_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam_concept_score
    ADD CONSTRAINT exam_concept_score_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exam(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE exam_result
DROP COLUMN date,
ADD COLUMN date_added timestamp,
ADD COLUMN last_updated timestamp;

CREATE TABLE public.group_concept_score (
    group_id integer NOT NULL,
    score double precision,
    concept_id integer NOT NULL
);
ALTER TABLE public.group_concept_score OWNER TO postgres;
--
-- Name: group_concept_score group_concept_score_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_concept_score
    ADD CONSTRAINT group_concept_score_pkey PRIMARY KEY (group_id, concept_id);


--
-- Name: group_concept_score group_concept_score_concept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_concept_score
    ADD CONSTRAINT group_concept_score_concept_id_fkey FOREIGN KEY (concept_id) REFERENCES public.concept(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: group_concept_score group_concept_score_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_concept_score
    ADD CONSTRAINT group_concept_score_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.usergroup(id) ON UPDATE CASCADE ON DELETE CASCADE;


CREATE TABLE public.group_course_score (
    group_id integer NOT NULL,
    score double precision,
    course_id integer NOT NULL
);
ALTER TABLE public.group_course_score OWNER TO postgres;

--
-- Name: group_course_score group_course_score_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_course_score
    ADD CONSTRAINT group_course_score_pkey PRIMARY KEY (group_id, course_id);


--
-- Name: group_course_score group_course_score_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_course_score
    ADD CONSTRAINT group_course_score_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.course(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: group_course_score group_course_score_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_course_score
    ADD CONSTRAINT group_course_score_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.usergroup(id) ON UPDATE CASCADE ON DELETE CASCADE;

CREATE TABLE public.group_exam_score (
    group_id integer NOT NULL,
    score double precision,
    exam_id integer NOT NULL
);


ALTER TABLE public.group_exam_score OWNER TO postgres;

--
-- Name: group_exam_score group_exam_score_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_exam_score
    ADD CONSTRAINT group_exam_score_pkey PRIMARY KEY (group_id, exam_id);


--
-- Name: group_exam_score group_exam_score_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_exam_score
    ADD CONSTRAINT group_exam_score_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exam(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: group_exam_score group_exam_score_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_exam_score
    ADD CONSTRAINT group_exam_score_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.usergroup(id) ON UPDATE CASCADE ON DELETE CASCADE;



ALTER TABLE permission
ADD COLUMN date_added timestamp,
ADD COLUMN last_updated timestamp;

ALTER TABLE permission_gen_api
ADD COLUMN date_added timestamp,
ADD COLUMN last_updated timestamp;

ALTER TABLE person
ADD COLUMN date_added timestamp,
ADD COLUMN last_updated timestamp;

ALTER TABLE question
ADD COLUMN date_added timestamp,
ADD COLUMN last_updated timestamp,
ADD COLUMN results_count integer,
ADD COLUMN number integer;

CREATE TABLE public.question_concept_score (
    question_id integer NOT NULL,
    score double precision,
    concept_id integer NOT NULL
);
ALTER TABLE public.question_concept_score OWNER TO postgres;

--
-- Name: question_concept_score question_concept_score_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_concept_score
    ADD CONSTRAINT question_concept_score_pkey PRIMARY KEY (question_id, concept_id);


--
-- Name: question_concept_score question_concept_score_concept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_concept_score
    ADD CONSTRAINT question_concept_score_concept_id_fkey FOREIGN KEY (concept_id) REFERENCES public.concept(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: question_concept_score question_concept_score_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_concept_score
    ADD CONSTRAINT question_concept_score_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.question(id) ON UPDATE CASCADE ON DELETE CASCADE;


ALTER TABLE question_result
ADD COLUMN date_added timestamp,
ADD COLUMN last_updated timestamp;

ALTER TABLE request_log
ADD COLUMN date_added timestamp,
ADD COLUMN last_updated timestamp;

ALTER TABLE role
ADD COLUMN date_added timestamp,
ADD COLUMN last_updated timestamp;

ALTER TABLE state_log
ADD COLUMN date_added timestamp,
ADD COLUMN last_updated timestamp;

ALTER TABLE "user"
ADD COLUMN date_added timestamp,
ADD COLUMN last_updated timestamp;

CREATE TABLE public.user_concept_score (
    user_key character varying(100) NOT NULL,
    score double precision,
    concept_id integer NOT NULL
);

ALTER TABLE public.user_concept_score OWNER TO postgres;

--
-- Name: user_concept_score user_concept_score_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_concept_score
    ADD CONSTRAINT user_concept_score_pkey PRIMARY KEY (user_key, concept_id);


--
-- Name: user_concept_score user_concept_score_concept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_concept_score
    ADD CONSTRAINT user_concept_score_concept_id_fkey FOREIGN KEY (concept_id) REFERENCES public.concept(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_concept_score user_concept_score_user_key_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_concept_score
    ADD CONSTRAINT user_concept_score_user_key_fkey FOREIGN KEY (user_key) REFERENCES public."user"(key) ON UPDATE CASCADE ON DELETE CASCADE;



CREATE TABLE public.user_course_score (
    user_key character varying(100) NOT NULL,
    score double precision,
    course_id integer NOT NULL
);

ALTER TABLE public.user_course_score OWNER TO postgres;

--
-- Name: user_course_score user_course_score_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_course_score
    ADD CONSTRAINT user_course_score_pkey PRIMARY KEY (user_key, course_id);


--
-- Name: user_course_score user_course_score_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_course_score
    ADD CONSTRAINT user_course_score_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.course(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_course_score user_course_score_user_key_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_course_score
    ADD CONSTRAINT user_course_score_user_key_fkey FOREIGN KEY (user_key) REFERENCES public."user"(key) ON UPDATE CASCADE ON DELETE CASCADE;

CREATE TABLE public.user_exam_score (
    user_key character varying(100) NOT NULL,
    score double precision,
    exam_id integer NOT NULL
);

ALTER TABLE public.user_exam_score OWNER TO postgres;

--
-- Name: user_exam_score user_exam_score_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_exam_score
    ADD CONSTRAINT user_exam_score_pkey PRIMARY KEY (user_key, exam_id);


--
-- Name: user_exam_score user_exam_score_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_exam_score
    ADD CONSTRAINT user_exam_score_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exam(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_exam_score user_exam_score_user_key_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_exam_score
    ADD CONSTRAINT user_exam_score_user_key_fkey FOREIGN KEY (user_key) REFERENCES public."user"(key) ON UPDATE CASCADE ON DELETE CASCADE;


ALTER TABLE usergroup
ADD COLUMN date_added timestamp,
ADD COLUMN last_updated timestamp;


--
-- Add permissions
-- role 4: admin, role 3 teacher, role 1 student
-- There are 23 permissions
--

INSERT INTO role (name) VALUES ('dev');

INSERT INTO permission (name) VALUES ('see_concepts');
INSERT INTO role_permissions (role_id, permission_id) VALUES (4, 24), (3, 24), (1, 24);
INSERT INTO permission (name) VALUES ('manage_concepts');
INSERT INTO role_permissions (role_id, permission_id) VALUES (3, 25);
INSERT INTO permission (name) VALUES ('see_concept_mapping');
INSERT INTO role_permissions (role_id, permission_id) VALUES (3, 26);
INSERT INTO permission (name) VALUES ('see_invisible_exams');
INSERT INTO role_permissions (role_id, permission_id) VALUES (3, 27);
INSERT INTO permission (name) VALUES ('manage_groups');
INSERT INTO role_permissions (role_id, permission_id) VALUES (3, 28);
INSERT INTO permission (name) VALUES ('see_groups');
INSERT INTO role_permissions (role_id, permission_id) VALUES (3, 29);
INSERT INTO permission (name) VALUES ('see_own_groups');
INSERT INTO role_permissions (role_id, permission_id) VALUES (1, 30);
INSERT INTO permission (name) VALUES ('see_user_groups');
INSERT INTO role_permissions (role_id, permission_id) VALUES (3, 31);
INSERT INTO permission (name) VALUES ('see_users');
INSERT INTO role_permissions (role_id, permission_id) VALUES (3, 32);
INSERT INTO permission (name) VALUES ('see_all_courses');
INSERT INTO role_permissions (role_id, permission_id) VALUES (4, 33);
INSERT INTO permission (name) VALUES ('manage_courses');
INSERT INTO role_permissions (role_id, permission_id) VALUES (4, 34);
INSERT INTO permission (name) VALUES ('see_courses');
INSERT INTO role_permissions (role_id, permission_id) VALUES (4, 35), (3, 35), (1, 35);
INSERT INTO permission (name) VALUES ('load_exam_results');
INSERT INTO role_permissions (role_id, permission_id) VALUES (3, 36);
INSERT INTO permission (name) VALUES ('use_dev_calls');
INSERT INTO role_permissions (role_id, permission_id) VALUES (6, 37);
INSERT INTO permission (name) VALUES ('generate_api_key');
INSERT INTO role_permissions (role_id, permission_id) VALUES (4, 38);
INSERT INTO permission (name) VALUES ('see_users_with_role');
INSERT INTO role_permissions (role_id, permission_id) VALUES (4, 39), (3, 39);
INSERT INTO permission (name) VALUES ('see_collection_hierarchy');
INSERT INTO role_permissions (role_id, permission_id) VALUES (4, 40);
INSERT INTO permission (name) VALUES ('invalidate_cache');
INSERT INTO role_permissions (role_id, permission_id) VALUES (6, 41);
INSERT INTO permission (name) VALUES ('reset_user_password');
INSERT INTO role_permissions (role_id, permission_id) VALUES (4, 42);

-- Give teacher permission to manage exams
INSERT INTO role_permissions (role_id, permission_id) VALUES (3, 6);

INSERT INTO collection (name, parent_id) VALUES ('remindo', 1);
