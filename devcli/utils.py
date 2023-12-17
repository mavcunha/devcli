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
