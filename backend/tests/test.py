"""
AI Report Generation Test
"""

import requests

BASE_URL = "http://127.0.0.1:8000"

DOCUMENT_ID = "7264efa3-ffa8-4eba-9c66-563cf77c10bf"

response = requests.post(
    f"{BASE_URL}/reports/generate/{DOCUMENT_ID}"
)

print("=" * 60)
print("KnowledgeOS AI")
print("AI Report Test")
print("=" * 60)

print("Status Code:", response.status_code)

if response.status_code == 200:

    report = response.json()

    print("✓ Report Generated Successfully\n")

    print("Title:")
    print(report["title"])

    print("\nSummary:")
    print(report["summary"])

    print("\nReport:")
    print(report["report"])

else:

    print("✗ Report Generation Failed")
    print(response.text)

print("=" * 60)