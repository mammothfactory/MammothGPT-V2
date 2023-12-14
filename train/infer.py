from transformers import (
    pipeline,
    logging,
)

logging.set_verbosity(logging.CRITICAL)

prompt = ""

pipe = pipeline(task="text-generation", model=model,tokenizer=tokenizer, max_length=200)
result = pipe(f"<s>[INST] {prompt} [/INST]")

print(result[0]['generated_text'])

