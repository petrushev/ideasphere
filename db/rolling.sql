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
