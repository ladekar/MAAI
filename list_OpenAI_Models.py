print ("My Code is for listing all the OpenAI Models via API")
print ("Created by Sunil Ladekar")
print ("Maai 2025")
print ("   ")

import subprocess

# Replace with your actual API key
api_key = "maai-project"

# Replace with the actual API verification URL
url = "https://api.openai.com/v1/models"

# Example curl command: curl -H "Authorization: Bearer your_api_key" -X GET https://api.openai.com/v1/models
#curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"
#echo $OPENAI_API_KEY
#your_OpenAI_api_key

response = subprocess.run(
    ["curl", "-H", f"Authorization: Bearer {api_key}", "-X", "GET", url],
    capture_output=True,
    text=True
)

if response.returncode == 0:
    print("API Response:", response.stdout)
else:
    print("Error:", response.stderr)

