import jinja2, markdown2, tomllib, re, pathlib


def load_config(cfg_str):
    return tomllib.loads(cfg_str)


def load_content():
    pass


def load_templates():
    pass


def app():
    cfg_str = pathlib.Path().cwd() / "config.toml"
    print(cfg_str)
    # config = load_config(cfg_str)
    # content = load_content()
    # templates = load_templates()

    # render(config, content, templates)


app()
