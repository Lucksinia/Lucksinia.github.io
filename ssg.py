import jinja2, markdown2, tomllib, re, pathlib, pprint
from datetime import datetime
import shutil

pp = pprint.PrettyPrinter(depth=2)


def load_config(cfg_file):
    with open(cfg_file, "rb") as configf:
        return tomllib.load(configf)


def load_content(content_dir):
    # list of posts
    posts = []
    item = {}
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
        # adding diferent dict because markdown2 is funky as hell and not allows posts into list
        # praised be standart dict impl as Ordered.
        item = content.metadata
        item["post"] = content
        posts.append(item)
    posts.sort(key=lambda x: x["date"], reverse=True)
    return posts


def load_templates(template_path):
    fs_loader = jinja2.FileSystemLoader(template_path)
    return jinja2.Environment(loader=fs_loader)


def create_render(config, content, env, output_dir):
    out_p = pathlib.Path(output_dir)
    if out_p.exists():
        shutil.rmtree(output_dir)
    out_p.mkdir()

    # index page for posts


def app():
    config = load_config("config.toml")
    # * pp.pprint(config)
    content = {"posts": load_content("content/posts")}
    # * pp.pprint(content)
    environment = load_templates("layout")
    create_render(config, content, environment, "public")


app()
