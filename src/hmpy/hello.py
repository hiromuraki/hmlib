class Hello:
    def __init__(self, name: str):
        self.name = name

    def say_hello(self) -> str:
        return f"Hello, {self.name}!"
