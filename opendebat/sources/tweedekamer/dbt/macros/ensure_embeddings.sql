{% macro ensure_embeddings_table() %}
    {% set database = 'tweedekamer2' %}
    {% set schema = target.schema %}

    CREATE TABLE IF NOT EXISTS {{ adapter.quote(database) }}.{{ adapter.quote(schema) }}.embeddings (
        _dlt_id TEXT,
        _dlt_load_id TEXT,
        embedding FLOAT[384],
    );
{% endmacro %}