from dlt.sources.filesystem import filesystem as filesystemsource, read_jsonl, readers
from sentence_transformers import SentenceTransformer
import numpy as np
import dlt
import duckdb


@dlt.source()
def verslagen_embeddings(
    lookup_path: str = "tweedekamer2.duckdb",
    db_batch_size: int = 10000,
    model_batch_size: int = 128,
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
):
    conn = duckdb.connect(lookup_path)
    model = SentenceTransformer(embedding_model)

    @dlt.resource(
        name="embeddings",
        table_name="embeddings",
        write_disposition="replace",
        columns={
            "_dlt_id": {"data_type": "text"},
            "embedding": {"data_type": "json"},
        },
    )
    def embeddings():
        reader = conn.execute(
            """
            SELECT
                _dlt_id,
                tekst,
            FROM tweedekamer2.segments.segments
            """
        ).fetch_record_batch(db_batch_size)

        for batch in reader:
            vectors = model.encode(
                batch["tekst"].to_pylist(), batch_size=model_batch_size
            ).astype(np.float32)

            for idx, vec in enumerate(vectors):
                yield {
                    "_dlt_id": batch["_dlt_id"][idx].as_py(),
                    "embedding": vec.tolist(),
                }

        conn.close()

    return embeddings
