CREATE TABLE urls(
	id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	name VARCHAR(255) UNIQUE,
	created_at DATE default NOW()
);