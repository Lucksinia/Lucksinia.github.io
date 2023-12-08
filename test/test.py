import markdown2, pathlib

path_to_test = pathlib.Path().cwd() / "content" / "posts" / "test-post.md"
path_to_output = pathlib.Path().cwd() / "test" / "out.html"
html = markdown2.markdown(str(path_to_test.open().read()), use_file_vars=True)
# path_to_output.write_text(str(html))
frontmatter = html.metadata
print(frontmatter)
