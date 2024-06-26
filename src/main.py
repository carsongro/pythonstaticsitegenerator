from htmlnode import HTMLNode
from textnode import markdown_to_blocks, markdown_to_html_node, block_to_block_type, block_type_heading
import shutil
import os

def main():
    copy_contents("static", "public")
    generate_pages_recursive("content", "template.html", "public")

def copy_contents(from_directory, to_directory):
    # remove contents from old directory    
    shutil.rmtree(f"{to_directory}", True)
    os.mkdir("public")

    def copy(from_directory, to_directory):
        paths = os.listdir(from_directory)
        for path in paths:
            isFile = os.path.isfile(os.path.join(from_directory, path))
            src, dst = os.path.join(from_directory, path), os.path.join(to_directory, path)
            if isFile:
                print(f"Copying: {src} to {dst}")
                shutil.copy(src, dst)
            else:
                os.mkdir(dst)
                copy(f"{src}", f"{dst}")
    
    copy(from_directory, to_directory)
    
def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == block_type_heading and block.startswith("# "):
            return block.removeprefix("# ")

    raise Exception("There must be a h1 header")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    f = open(from_path)
    file_contents = f.read()
    f.close()

    t = open(template_path)
    template_contents = t.read()
    t.close()

    node = markdown_to_html_node(file_contents)
    html = node.to_html()
    title = extract_title(file_contents)
    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html)

    dir = os.path.dirname(dest_path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    n = open(dest_path, "x")
    n.write(template_contents)
    n.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_directory = os.listdir(dir_path_content)

    def md_to_html(from_path):
        components = from_path.split("/")
        components[-1] = components[-1].replace(".md", ".html")
        return "/".join(components)

    def write(from_directory, to_directory):
        paths = os.listdir(from_directory)
        for path in paths:
            isFile = os.path.isfile(os.path.join(from_directory, path))
            src, dst = os.path.join(from_directory, path), md_to_html(os.path.join(to_directory, path))
            if isFile:
                print(f"Copying: {src} to {dst}")
                generate_page(src, template_path, dst)
            else:
                os.mkdir(dst)
                write(f"{src}", f"{dst}")

    write(dir_path_content, dest_dir_path)


if __name__ == '__main__':
    main()