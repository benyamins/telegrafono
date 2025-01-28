import typer
from .config import load_config, get_logger
from .telebot import application_builder

app = typer.Typer()


@app.command()
def start():
    config = load_config()
    logger = get_logger(__name__)
    logger.info("String the bot")
    app = application_builder(config.token)
    app.run_polling()


@app.command()
def self():
    config = load_config()
    typer.echo(f"Config: {config}")
