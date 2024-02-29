from typing import List, Optional

import fire


from llama import Llama, Dialog

ckpt_dir = "llama/llama-2-7b"
tokenizer_path = "llama/tokenizer.model"
temperature = 0.6
top_p  = 0.9
max_seq_len = 1024
max_batch_size = 8
max_gen_len = None

generator = Llama.build(
    ckpt_dir=ckpt_dir,
    tokenizer_path=tokenizer_path,
    max_seq_len=max_seq_len,
    max_batch_size=max_batch_size,
)

dialogs = [{"role": "user", "content" : "Tell me why mayonaise is so good."}]
results = generator.chat_completion(
        dialogs,  # type: ignore
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )

for dialog, result in zip(dialogs, results):
    for msg in dialog:
        print(f"{msg['role'].capitalize()}: {msg['content']}\n")
    print(
        f"> {result['generation']['role'].capitalize()}: {result['generation']['content']}"
    )
    print("\n==================================\n")