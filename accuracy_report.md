# Accuracy Test Report 🤖
Generated on: 2026-03-13 16:26:10

## Summary
- **Total Test Cases**: 10
- **Passed**: 10
- **Failed**: 0
- **Accuracy**: 100.00%

## Detailed Results
| Query | Expected Intent | Actual Intent | Expected Params | Actual Params | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| What is the weather in London? | weather | weather | {"city": "london"} | {"city": "london"} | ✅ PASS |
| weather in Tokyo | weather | weather | {"city": "tokyo"} | {"city": "tokyo"} | ✅ PASS |
| How is the temperature in New York? | weather | weather | {"city": "new york"} | {"city": "new york"} | ✅ PASS |
| Convert 100 USD to EUR | currency | currency | {"amount": "100", "from": "usd", "to": "eur"} | {"amount": "100", "from": "usd", "to": "eur"} | ✅ PASS |
| 150 pounds to naira | currency | currency | {"amount": "150", "from": "pounds", "to": "naira"} | {"amount": "150", "from": "pounds", "to": "naira"} | ✅ PASS |
| What is 50.5 CAD in USD? | currency | currency | {"amount": "50.5", "from": "cad", "to": "usd"} | {"amount": "50.5", "from": "cad", "to": "usd"} | ✅ PASS |
| Hi there! | greeting | greeting | {} | {} | ✅ PASS |
| Can you help me? | greeting | greeting | {} | {} | ✅ PASS |
| Who is the president of France? | fallback | fallback | {} | {} | ✅ PASS |
| Tell me a joke | fallback | fallback | {} | {} | ✅ PASS |
