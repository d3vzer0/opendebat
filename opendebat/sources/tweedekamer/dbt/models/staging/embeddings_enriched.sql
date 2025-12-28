{{ config(
    materialized='table',
    post_hook = [
        "{{ ensure_embeddings_table() }}",
        "INSTALL vss;",
        "LOAD vss;",
        "SET GLOBAL hnsw_enable_experimental_persistence = true;",
        "CREATE INDEX IF NOT EXISTS ip_idx ON {{ source('segments', 'segments_enriched') }} USING HNSW (embedding) WITH (metric = 'ip');"
    ]
    ) 
}}

SELECT 
    n._dlt_load_id,
    n._dlt_id,
    s.vergadering_titel,
    s.activiteit_titel,
    s.spreker,
    s.tijdstip_start,
    s.tijdstip_eind,
    s.tekst,
    CAST(n.embedding AS FLOAT[384]) as embedding,
FROM {{ source('segments', 'embeddings') }} n
JOIN {{ source('segments', 'segments') }} s ON n._dlt_id = s._dlt_id