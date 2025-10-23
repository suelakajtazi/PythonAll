from typing import Optional
from typing import Any
from typing import Union
from typing import List

def process(value : Any) -> str:
    return f"processed{value}"

print(process("digital school"))

def process_value(value: Union[int,str]) -> str:
    if isinstance(value,int):
        return f"number {value}"
    return f"string {value}"

print(process_value)

  