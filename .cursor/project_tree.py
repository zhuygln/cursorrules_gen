import os
import json
from pathlib import Path

def build_tree(directory='.', exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = {'.git', '__pycache__', 'venv', 'build', 'dist', '*.egg-info'}
    
    path = Path(directory)
    tree = {
        "name": path.name or str(path),
        "type": "directory",
        "children": []
    }
    
    try:
        for item in sorted(path.iterdir()):
            if any(ex in str(item) for ex in exclude_dirs):
                continue
                
            if item.is_dir():
                tree["children"].append(build_tree(item, exclude_dirs))
            else:
                tree["children"].append({
                    "name": item.name,
                    "type": "file",
                    "extension": item.suffix[1:] if item.suffix else None
                })
    except PermissionError:
        pass
        
    return tree

def create_html_visualization(tree, output_path='.cursor/project_structure.html'):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .tree { font-family: monospace; }
            .dir { color: #4286f4; }
            .file { color: #555; }
            .tree ul { list-style: none; }
            .tree li::before { content: "├── "; }
        </style>
    </head>
    <body>
    <div class="tree">
    """
    
    def add_node(node, level=0):
        indent = "&nbsp;" * 4 * level
        class_name = "dir" if node["type"] == "directory" else "file"
        html_parts.append(f'<div>{indent}<span class="{class_name}">{node["name"]}</span></div>')
        if node["type"] == "directory":
            for child in node["children"]:
                add_node(child, level + 1)
    
    html_parts = []
    add_node(tree)
    html += "\n".join(html_parts)
    html += """
    </div>
    </body>
    </html>
    """
    
    with open(output_path, 'w') as f:
        f.write(html)

def save_tree():
    # Create .cursor directory if it doesn't exist
    os.makedirs('.cursor', exist_ok=True)
    
    # Build and save JSON structure
    tree = build_tree()
    with open('.cursor/project_structure.json', 'w') as f:
        json.dump(tree, f, indent=2)
    
    # Save text version
    with open('.cursor/project_structure.txt', 'w') as f:
        def print_tree(node, level=0):
            prefix = '│   ' * level + '├── '
            print(f"{prefix}{node['name']}", file=f)
            if node['type'] == 'directory':
                for child in node['children']:
                    print_tree(child, level + 1)
        print_tree(tree)
    
    # Create HTML visualization
    create_html_visualization(tree)

if __name__ == '__main__':
    save_tree()

# Run this to see your structure
tree = build_tree()
print(json.dumps(tree, indent=2)) 