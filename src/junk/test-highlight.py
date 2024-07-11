"""
This example demonstrates a simple text highlighter.
"""

from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.theme import Theme


class EmailHighlighter(RegexHighlighter):
    """Apply style to anything that looks like an email."""

    base_style = "example."
    highlights = [
        r"(?i)(?P<learn>learn[a-z]+|lesson|ml|train[a-z]+|ml)",
        r"(?i)(?P<machine>machine|computer)",
        r"(?i)(?P<model>model[a-z]*|embed[a-z]*)",
    ]


theme = Theme(
    {"example.learn": "bold magenta",
     "example.machine": "bold green",
     "example.model": "bold blue",
     })
console = Console(highlighter=EmailHighlighter(), theme=theme)

console.print("ML models for computer machine learning lessons and training with embeddings")

print("Done!")
