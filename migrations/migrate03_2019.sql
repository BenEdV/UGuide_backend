ALTER TABLE study_material
ADD COLUMN course_id integer,
ADD CONSTRAINT study_material_course_id_fkey FOREIGN KEY (course_id) REFERENCES course (id);
