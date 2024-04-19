
CREATE TABLE account (
	id UUID NOT NULL, 
	email VARCHAR NOT NULL, 
	password VARCHAR NOT NULL, 
	name VARCHAR NOT NULL, 
	last_name VARCHAR NOT NULL, 
	username VARCHAR NOT NULL, 
	birthday DATE, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	UNIQUE (email), 
	UNIQUE (username)
)


CREATE TABLE school_grade (
	id SERIAL NOT NULL, 
	year INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (year)
)


CREATE TABLE subject_type (
	id SERIAL NOT NULL, 
	name VARCHAR NOT NULL, 
	handle VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name), 
	UNIQUE (handle)
)


CREATE TABLE absence (
	id SERIAL NOT NULL, 
	account_id UUID NOT NULL, 
	start_time TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	end_time TIMESTAMP WITHOUT TIME ZONE, 
	date DATE NOT NULL, 
	reason VARCHAR, 
	excused BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(account_id) REFERENCES account (id)
)


CREATE TABLE access_token (
	id UUID NOT NULL, 
	account_id UUID NOT NULL, 
	expiration_date TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	creation_date TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(account_id) REFERENCES account (id)
)


CREATE TABLE contact (
	id SERIAL NOT NULL, 
	account_id UUID NOT NULL, 
	contact_type VARCHAR, 
	contact VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(account_id) REFERENCES account (id)
)


CREATE TABLE parent (
	id SERIAL NOT NULL, 
	account_id UUID NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (account_id), 
	FOREIGN KEY(account_id) REFERENCES account (id)
)


CREATE TABLE su (
	id SERIAL NOT NULL, 
	account_id UUID NOT NULL, 
	admin_rights BOOLEAN NOT NULL, 
	change_subject_status BOOLEAN NOT NULL, 
	manage_users BOOLEAN NOT NULL, 
	manage_school BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (account_id), 
	FOREIGN KEY(account_id) REFERENCES account (id)
)


CREATE TABLE teacher (
	id SERIAL NOT NULL, 
	account_id UUID NOT NULL, 
	abbreviation VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (account_id), 
	FOREIGN KEY(account_id) REFERENCES account (id), 
	UNIQUE (abbreviation)
)


CREATE TABLE school_class (
	id SERIAL NOT NULL, 
	name VARCHAR NOT NULL, 
	grade_id INTEGER NOT NULL, 
	head_teacher_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(grade_id) REFERENCES school_grade (id), 
	FOREIGN KEY(head_teacher_id) REFERENCES teacher (id)
)


CREATE TABLE school_subject (
	id SERIAL NOT NULL, 
	teacher_id INTEGER NOT NULL, 
	subject_type_id INTEGER NOT NULL, 
	week_day INTEGER NOT NULL, 
	timeslot INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(teacher_id) REFERENCES teacher (id), 
	FOREIGN KEY(subject_type_id) REFERENCES subject_type (id)
)


CREATE TABLE school_subject_entry (
	id SERIAL NOT NULL, 
	teacher_id INTEGER, 
	subject_id INTEGER NOT NULL, 
	date DATE NOT NULL, 
	note VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(teacher_id) REFERENCES teacher (id), 
	FOREIGN KEY(subject_id) REFERENCES school_subject (id)
)


CREATE TABLE student (
	id SERIAL NOT NULL, 
	account_id UUID NOT NULL, 
	school_class_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (account_id), 
	FOREIGN KEY(account_id) REFERENCES account (id), 
	FOREIGN KEY(school_class_id) REFERENCES school_class (id)
)


CREATE TABLE homework (
	id SERIAL NOT NULL, 
	subject_entry INTEGER NOT NULL, 
	content VARCHAR NOT NULL, 
	due_date DATE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(subject_entry) REFERENCES school_subject_entry (id)
)


CREATE TABLE parent_student (
	id SERIAL NOT NULL, 
	parent_id INTEGER NOT NULL, 
	student_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(parent_id) REFERENCES parent (id), 
	FOREIGN KEY(student_id) REFERENCES student (id)
)


CREATE TABLE school_subject_student (
	id SERIAL NOT NULL, 
	student_id INTEGER NOT NULL, 
	subject_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(student_id) REFERENCES student (id), 
	FOREIGN KEY(subject_id) REFERENCES school_subject (id)
)


CREATE TABLE homework_status (
	id SERIAL NOT NULL, 
	homework_id INTEGER NOT NULL, 
	student_id INTEGER NOT NULL, 
	status BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(homework_id) REFERENCES homework (id), 
	FOREIGN KEY(student_id) REFERENCES student (id)
)

