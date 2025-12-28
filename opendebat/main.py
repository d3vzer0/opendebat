import typer
from opendebat.cli.collect import collect

app = typer.Typer(pretty_exceptions_enable=False)
app.add_typer(collect, name="collect")

if __name__ == "__main__":
    app()
