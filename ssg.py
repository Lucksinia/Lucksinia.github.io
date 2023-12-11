import jinja2, markdown2, tomllib, re, pathlib
from datetime import datetime


def load_config(cfg_file):
    with open(cfg_file, "rb") as configf:
        return tomllib.load(configf)


def load_content(content_dir):
    posts = []
    path = pathlib.Path.cwd()
    for file in path.glob(f"{content_dir}/*.md"):
        content = markdown2.markdown(
            str(file.open().read()),
            use_file_vars=True,
        )
        content.metadata["date"] = datetime.fromisoformat(content.metadata["date"])

        content.metadata["slug"] = file.name.removesuffix(".md")
        content.metadata[
            "url"
        ] = f"/{content.metadata['date'].year}/{content.metadata['slug']}"
        print(content.metadata)
        posts.append(content)
    posts.sort(key=lambda x: x.metadata["date"], reverse=True)
    return posts


def load_templates():
    pass


def app():
    config = load_config("config.toml")
    content = load_content("content/posts")
    # templates = load_templates()

    # render(config, content, templates)


app()
