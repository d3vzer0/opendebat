{% macro ensure_embeddings_table() %}

    CREATE TABLE IF NOT EXISTS {{ source('segments', 'segments_enriched') }} (
        _dlt_id TEXT,
        _dlt_load_id TEXT,
        vergadering_titel TEXT,
        activiteit_titel TEXT,
        spreker TEXT,
        tijdstip_start TEXT,
        tijdstip_eind TEXT,
        tekst TEXT,
        embedding FLOAT[384],
    );
{% endmacro %}