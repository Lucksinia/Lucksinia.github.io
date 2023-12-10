import jinja2, markdown2, tomllib, re, pathlib


def load_config(cfg_file):
    with open(cfg_file, "rb") as configf:
        return tomllib.load(configf)


def load_content(content_dir):
    items = []
    path = pathlib.Path.cwd()
    for file in path.glob(f"{content_dir}/*.md"):
        print(file)


def load_templates():
    pass


def app():
    config = load_config("config.toml")
    content = load_content("content/posts")
    # templates = load_templates()

    # render(config, content, templates)


app()
