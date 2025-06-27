def generic_message(example="string"):
    return {
        "content": {"text/plain": {"schema": {"type": "string", "example": example}}}
    }
