import requests


url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
payload = {
    "name": "John Doe",
    "regNo": "REG12347",
    "email": "john@example.com"
}

response = requests.post(url, json=payload)
response_data = response.json()


webhook_url = response_data.get("webhook")
access_token = response_data.get("accessToken")

final_sql_query = """
SELECT 
    p.AMOUNT AS SALARY,
    CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
    FLOOR(DATEDIFF(CURDATE(), e.DOB) / 365) AS AGE,
    d.DEPARTMENT_NAME
FROM 
    PAYMENTS p
JOIN 
    EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN 
    DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE 
    DAY(p.PAYMENT_TIME) != 1
ORDER BY 
    p.AMOUNT DESC
LIMIT 1;
"""

headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}
submit_payload = {
    "finalQuery": final_sql_query.strip()
}

submit_response = requests.post(webhook_url, json=submit_payload, headers=headers)
print("Submission Response:", submit_response.status_code, submit_response.text)
