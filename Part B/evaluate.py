import json
import re
import urllib.request

MODEL = "qwen2.5:0.5b-instruct"
URL = "http://localhost:11434/api/generate"

TEMPERATURE = 0
MAX_TOKENS = 128


def normalize(text):
    """Lowercase and remove punctuation."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.split()


def similarity(prediction, expected):
    """Simple word-overlap score. Just to see which words appear"""
    pred_words = set(normalize(prediction))
    expected_words = set(normalize(expected))

    if not expected_words:
        return 0

    return len(pred_words & expected_words) / len(expected_words)


def ask_model(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": TEMPERATURE,
            "num_predict": MAX_TOKENS
        }
    }

    req = urllib.request.Request(
        URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())

    return result["response"].strip()


# Load test cases
with open("test.jsonl", "r") as f:
    tests = [json.loads(line) for line in f]

results = []
pass_count = 0
partial_count = 0
fail_count = 0

for test in tests:
    print(f"Running {test['id']}...")

    try:
        prediction = ask_model(test["input"])

        if prediction.lower() == test["expected"].lower():
            status = "PASS"
            score = 1.0
            pass_count += 1

        else:
            score = similarity(prediction, test["expected"])

            if score >= 0.6: #threshold of 0.6
                status = "PARTIAL"
                partial_count += 1
            else:
                status = "FAIL"
                fail_count += 1

        results.append({
            "id": test["id"],
            "input": test["input"],
            "expected": test["expected"],
            "prediction": prediction,
            "status": status,
            "score": round(score, 2)
        })

    except Exception as e:
        fail_count += 1

        results.append({
            "id": test["id"],
            "input": test["input"],
            "expected": test["expected"],
            "prediction": "",
            "status": "ERROR",
            "score": 0,
            "reason": str(e)
        })

# Summary
total = len(tests)

print("\n========== SUMMARY ==========")
print(f"Total Tests : {total}")
print(f"PASS        : {pass_count}")
print(f"PARTIAL     : {partial_count}")
print(f"FAIL/ERROR  : {fail_count}")
print(f"Pass Rate   : {(pass_count + partial_count) / total * 100:.1f}%")

print("\n========== FAILURES ==========")

for r in results:
    if r["status"] in ("FAIL", "ERROR"):
        print(f"\nID: {r['id']}")
        print(f"Question : {r['input']}")
        print(f"Expected : {r['expected']}")
        print(f"Prediction : {r['prediction']}")
        if "reason" in r:
            print(f"Reason : {r['reason']}")
        else:
            print(f"Similarity : {r['score']}")

# Save results
with open("results.json", "w") as f:
    json.dump(results, f, indent=4)

print("\nResults saved to results.json")