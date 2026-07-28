# This script (evaluate.py) evaluates qwen2.5:0.5b-instruct against the given JSONL test set (test.jsonl).

## How to run it
```bash
python evaluate.py
```

# Parameters
- **Temperature:** `0` Because this is an evaluation tool, we want reproducibility so temperature is set to 0 for no creativity of the model.
- **Max Tokens:** `128`: 128 tokens is sufficient for the expected responses while avoiding unnecessarily long generations.

# Scoring - This is assuming we used the same policy rules as we defined earlier in Part A
### Exact match (lower-case, punctuation, white-space all removed) -> Pass 
### Partial match -> depends on threshold (I set threshold of 0.6) to be counted as -> Partial
#### How does this work? Score = number of matching words / number of words in expected answer
### No match (anything less than 0.6) -> Fail
