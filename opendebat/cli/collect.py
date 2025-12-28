from opendebat.sources.tweedekamer.source import tweedekamer
from opendebat.sources.tweedekamer.embeddings import verslagen_embeddings
import typer
import dlt
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]


collect = typer.Typer()


@collect.command()
def verslag():
    pipeline = dlt.pipeline(
        pipeline_name="tweedekamer2",
        destination="duckdb",
        dataset_name="segments",
        progress="enlighten",
    )

    pipeline.run(tweedekamer(), write_disposition="replace")


@collect.command()
def embeddings():
    pipeline = dlt.pipeline(
        pipeline_name="tweedekamer2",
        destination="duckdb",
        dataset_name="segments",
        progress="enlighten",
    )

    # pipeline.run(verslagen_embeddings(), write_disposition="replace")

    dbt = dlt.dbt.package(
        pipeline, str(PACKAGE_ROOT.joinpath("sources", "tweedekamer", "dbt"))
    )
    dbt.run_all()
