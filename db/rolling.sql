CREATE TABLE "user"
(
  id serial NOT NULL,
  service_id character varying(128) NOT NULL,
  service character varying(8) NOT NULL,
  display_name character varying(128),
  fullname character varying(128),
  email character varying(64),
  CONSTRAINT p_user PRIMARY KEY (id),
  CONSTRAINT u_user UNIQUE (service_id, service)
)
WITH (
  OIDS=FALSE
);

CREATE TABLE "comment"
(
  "time" timestamp without time zone NOT NULL,
  user_id integer NOT NULL,
  page_id text NOT NULL,
  content text NOT NULL,
  CONSTRAINT p_comment PRIMARY KEY ("time", user_id),
  CONSTRAINT fk_comment_user FOREIGN KEY (user_id)
      REFERENCES "user" (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE RESTRICT
)
WITH (
  OIDS=FALSE
);

ALTER TABLE "user"
   ADD COLUMN img_url text;

CREATE TABLE mission
(
   id bigserial NOT NULL,
   title text NOT NULL,
   meta text,
   CONSTRAINT p_mission PRIMARY KEY (id),
   CONSTRAINT u_mission UNIQUE (title)
)
WITH (
  OIDS = FALSE
);

CREATE TABLE problem
(
   id bigserial NOT NULL,
   mission_id bigint NOT NULL,
   title text NOT NULL,
   meta text NOT NULL,
   CONSTRAINT p_problem PRIMARY KEY (id),
   CONSTRAINT fk_problem_mission FOREIGN KEY (mission_id)
      REFERENCES mission (id)
      ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT u_problem UNIQUE (mission_id, title)
)
WITH (
  OIDS = FALSE
);

ALTER TABLE mission
   ADD COLUMN created timestamp without time zone NOT NULL;

ALTER TABLE problem
   ADD COLUMN created timestamp without time zone NOT NULL;

ALTER TABLE "user"
   ADD COLUMN is_admin boolean;
update "user"
   set is_admin = false;
ALTER TABLE "user"
   ALTER COLUMN is_admin SET NOT NULL;

CREATE TABLE public.proposal
(
   id bigserial NOT NULL,
   problem_id bigint NOT NULL,
   user_id integer NOT NULL,
   submited timestamp without time zone NOT NULL,
   title text,
   description text,
   img text,
   model text,
   CONSTRAINT p_proposal PRIMARY KEY (id),
   CONSTRAINT fk_proposal_problem FOREIGN KEY (problem_id)
      REFERENCES problem (id)
      ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT fk_proposal_user FOREIGN KEY (user_id)
      REFERENCES "user" (id)
      ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT u_proposal UNIQUE (user_id, submited)
)
WITH (
  OIDS = FALSE
);

CREATE TABLE public.vote
(
   user_id bigint NOT NULL,
   proposal_id bigint NOT NULL,
   is_plus boolean NOT NULL DEFAULT true,
   CONSTRAINT p_vote PRIMARY KEY (user_id, proposal_id),
   CONSTRAINT fk_vote_user FOREIGN KEY (user_id)
      REFERENCES "user" (id)
      ON UPDATE CASCADE ON DELETE RESTRICT,
   CONSTRAINT fk_vote_proposal FOREIGN KEY (proposal_id)
      REFERENCES proposal (id)
      ON UPDATE CASCADE ON DELETE RESTRICT
)
WITH (
  OIDS = FALSE
);
