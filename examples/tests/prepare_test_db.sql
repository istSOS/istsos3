-- Fill table with random data

delete from data._4d77a90e4ffa11e798b5e0db55c4a7a5;
insert into data._4d77a90e4ffa11e798b5e0db55c4a7a5
    (event_time, _9, _9_qi, _10, _10_qi)
    (
        select
        '2006-01-01T00:00:00+01'::timestamp with time zone + s * interval '10 minutes' as event_time,
        random() * 40,
        (random() * 5 + 100)::int,
        random() * 40,
        (random() * 5 + 100)::int
        from generate_Series(1,10512000) as s
    );
