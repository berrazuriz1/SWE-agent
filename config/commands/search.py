import sys
import hashlib
import os
from blar_graph.graph_construction.core.graph_builder import GraphConstructor
from blar_graph.db_managers import Neo4jManager


def format_print(code_lines, start_line):
    # Print formatted output
    print("Current node code:")
    for i, line in enumerate(code_lines, start=start_line):
        print(f"{i}: {line}")


def search_graph(query: str):
    repo_name = os.getenv("REPO_NAME")
    repo_id = hashlib.sha256(repo_name.encode()).hexdigest()
    graph_manager = Neo4jManager(repo_id)
    code, neighbours = graph_manager.get_code(query)
    code_text = code.get("node.text", "")
    start_line = code.get("node.start_line", 0)
    end_line = code.get("node.end_line", "")
    neighbours = neighbours
    path = code.get("node.path", "")
    code_lines = code_text.split("\n")

    print(f"[File: {path}]")
    format_print(code_lines, start_line)
    print(f"\nCurrent Line {start_line} - {end_line}")
    print(f"\nCurrent node neighbours: {neighbours}")

    os.environ["CURRENT_LINE"] = str(start_line)
    os.environ["CURRENT_FILE"] = path


if __name__ == "__main__":
    query = sys.argv[1]
    search_graph(query)
