import jinja2, markdown2, tomllib, re, pprint
from datetime import datetime
from pathlib import Path
import shutil

pp = pprint.PrettyPrinter(depth=2)


def load_config(cfg_file):
    with open(cfg_file, "rb") as configf:
        return tomllib.load(configf)


def load_content(content_dir: str):
    """Parse markdown with markdown2 capabilities in a content directory.
    as it uses "use-file-vars", don't forget to use markdown variables
    from within your file.

    :param str content_dir: Pathlike string pointing to the content
    directory
    :return dict: dictionary with [slug], [date], [posts] as html and
    [title]
    """
    # list of posts
    posts = []
    item = {}
    path = Path.cwd()
    for file in path.glob(f"{content_dir}/*.md"):
        content = markdown2.markdown(
            str(file.open().read()),
            use_file_vars=True,
        )
        content.metadata["date"] = datetime.fromisoformat(
            content.metadata["date"]
        ).date()

        content.metadata["slug"] = file.name.removesuffix(".md")
        content.metadata[
            "url"
        ] = f"/{content.metadata['date'].year}/{content.metadata['slug']}/"
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
    out_p = Path(output_dir)
    if out_p.exists():
        shutil.rmtree(output_dir)
    out_p.mkdir()
    cname = out_p / "CNAME"
    cname.touch()
    cname.write_text("lucksiniais.online")

    # index page for posts
    index_path = out_p / "index.html"
    index_template = env.get_template("index.html")
    index_path.write_text(index_template.render(config=config, content=content))

    # post pages loading
    post_template = env.get_template("post.html")
    for item in content["posts"]:
        post_url_str = output_dir + item["url"]
        post_url = Path(post_url_str)
        post_url.mkdir(parents=True, exist_ok=True)
        post_file = post_url / "index.html"
        post_file.touch()
        post_file.write_text(post_template.render(this=item, config=config))

    shutil.copytree("static", "public/static")


def app():
    config = load_config("config.toml")
    # * pp.pprint(config)
    content = {"posts": load_content("content/posts")}
    # * pp.pprint(content)
    environment = load_templates("layout")
    create_render(config, content, environment, "public")


app()
