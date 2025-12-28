from opendebat.sources.tweedekamer.source import tweedekamer
import typer
import dlt


collect = typer.Typer()


@collect.command()
def verslag():
    pipeline = dlt.pipeline(
        pipeline_name="tweedekamer",
        destination="duckdb",
        dataset_name="debatten",
        progress="enlighten",
    )

    pipeline.run(tweedekamer(), write_disposition="replace")
