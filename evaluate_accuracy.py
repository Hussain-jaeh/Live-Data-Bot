import json
import os
from chatbot_logic import process_prompt
from datetime import datetime

def evaluate():
    test_cases_path = "test_cases.json"
    if not os.path.exists(test_cases_path):
        print(f"Error: {test_cases_path} not found.")
        return

    with open(test_cases_path, "r") as f:
        test_cases = json.load(f)

    results = []
    passed = 0
    total = len(test_cases)

    for case in test_cases:
        query = case["query"]
        expected_intent = case["expected_intent"]
        expected_params = case["expected_parameters"]

        actual_intent, actual_params, _ = process_prompt(query)

        # Check accuracy
        intent_match = (actual_intent == expected_intent)
        params_match = (actual_params == expected_params)
        
        is_correct = intent_match and params_match
        if is_correct:
            passed += 1

        results.append({
            "query": query,
            "expected_intent": expected_intent,
            "actual_intent": actual_intent,
            "expected_params": expected_params,
            "actual_params": actual_params,
            "status": "✅ PASS" if is_correct else "❌ FAIL"
        })

    accuracy = (passed / total) * 100 if total > 0 else 0

    # Generate Report
    report_content = f"""# Accuracy Test Report 🤖
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary
- **Total Test Cases**: {total}
- **Passed**: {passed}
- **Failed**: {total - passed}
- **Accuracy**: {accuracy:.2f}%

## Detailed Results
| Query | Expected Intent | Actual Intent | Expected Params | Actual Params | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""

    for r in results:
        report_content += f"| {r['query']} | {r['expected_intent']} | {r['actual_intent']} | {json.dumps(r['expected_params'])} | {json.dumps(r['actual_params'])} | {r['status']} |\n"

    report_path = "accuracy_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"Evaluation complete. Accuracy: {accuracy:.2f}%. Report generated at {report_path}")

if __name__ == "__main__":
    evaluate()
