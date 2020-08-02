import logging

from psycopg2._psycopg import DatabaseError

from components.utils import _database_connect
from webchecker import settings


def forwards():

    # creating database tables
    conn, cursor = _database_connect(
        database=settings.DATABASE.database,
        user=settings.DATABASE.username,
        password=settings.DATABASE.password,
        host=settings.DATABASE.hostname,
        port=settings.DATABASE.port,
    )

    sql = """
        begin;

        drop trigger if exists insert_webchecker_checks_trigger on webchecker_checks;
        drop function if exists checks_insert();
        drop table if exists webchecker_checks cascade;
        
        create table webchecker_checks(
            id bigserial primary key,
            ts bigint not null,
            inserted_at timestamp default current_timestamp,
            response_time_seconds real not null,
            match_pattern boolean not null,
            status_code int not null,
            url text
        );
        
        create index  "idx_url" on webchecker_checks using btree (url);
        
        create or replace function checks_insert() 
        returns trigger as $$
        declare
            table_name varchar;
            date_timestamp timestamp;
            ts_begin bigint;
            ts_end bigint;
        begin
            date_timestamp := to_timestamp(new.ts) at time zone 'UTC';
            table_name := format('webchecker_checks_%s_%s', extract(year from date_timestamp), extract(month from date_timestamp));
            perform 1 from pg_class where relname = table_name limit 1;
            if not found
            then
                ts_begin := extract(epoch from date_trunc('month', date_timestamp));
                ts_end := extract(epoch from (date_trunc('month', date_timestamp) + interval '1 month'));
                execute format('create table %s (like webchecker_checks including all)', table_name);
                execute format('alter table %s inherit webchecker_checks, add check (ts >= %s and ts < %s)', 
                    table_name, ts_begin, ts_end);
                execute format('create index idx_%s_ts on %s (ts);', table_name, table_name);
            end if;
            execute 'insert into ' || table_name || ' values ( ($1).* )' using new;
            return null;
        end;
        $$ 
        language plpgsql;
        
        create trigger insert_webchecker_checks_trigger before insert on webchecker_checks for each row execute procedure checks_insert();
        
        commit;
    """
    try:
        cursor.execute(sql)
        conn.close()
    except DatabaseError:
        logging.error('An error occurred with the database')
        raise
