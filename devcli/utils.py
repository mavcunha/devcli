from io import StringIO

from rich.console import Console


class MissConfError(Exception):
    def __init__(self, topic, entry, example):
        self.topic = topic
        self.entry = entry
        self.example = example
        super().__init__(self._generate_message())

    def _generate_message(self):
        return (f"Missing entry '{self.entry}' on '{self.topic}'.\n"
                f"Ensure you have the following in your configuration:\n\n"
                f"[{self.topic}]\n"
                f"{self.entry} = {self.example}\n")


def styled_text(text: str, sty: str = None, end: str = ""):
    out = StringIO()
    console = Console(file=out, force_terminal=True)
    console.print(text, style=sty, end=end)
    return out.getvalue()
