class _Logger:
   def __init__(self, name: str):
       self.name = name

   def info(self, msg: str) -> None:
       print(f"[INFO] {self.name}: {msg}")

   def error(self, msg: str) -> None:
       print(f"[ERROR] {self.name}: {msg}")

   def debug(self, msg: str) -> None:
       print(f"[DEBUG] {self.name}: {msg}") 

   def warning(self, msg: str) -> None:
       print(f"[WARN] {self.name}: {msg}")



logger = _Logger('squire')