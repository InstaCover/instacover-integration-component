Calling AUTH endpoint using client_id (XXXXXXX lower) and client_secret (YYYYYYY lower) you will generate auth token, which you will use for calling API directly - for example for vehicle inspection session creation (lower).

```python
import requests

url = "https://api.instacover.ai/oauth/v1.0/token"

payload = 'grant_type=client_credentials&client_id=XXXXXXX&client_secret=YYYYYYY&scope=categorization'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
# response example
{
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnQiOnsiY2xpZW50SWQiOiIyNDk2MDViMC04OTFiLTExZWUtYjlkMS0wMjQyYWMxMjAwMDIiLCJvcmdhbml6YXRpb24iOiJ3w7xzdGVucm90LXNrIiwiZW52aXJvbm1lbnQiOiJwcm9kdWN0aW9uIn0sInVzZXIiOnt9LCJzY29wZXMiOiJjYXRlZ29yaXphdGlvbiIsImlhdCI6MTcwMDY0NjM1NCwiZXhwIjoxNzAwNjQ5OTU0LCJpc3MiOiJpbnN0YWNvdmVyLmFpLiJ9.SS-eAGXwXH9tL_fbNxyWoV33iFOaO4VT_JIoTwWMRrFTB5ZOdXyyfZL2tpslPrf0oUQ-nEcVxj68wqcdKn0lCuUAIKSxzyWLXvHoMI58kgtSRRxdmOjxTmMVwArHC7qBeOR1aVQD9P2xBZiz0PuyPWibkT38W9vgurlP7yuIwy7WlGXOJ63zMBHgdyIS9MHw1PC-PxEwr6jTDsbSMTu80IdzynY96PHm6S8T9QeD0bMCyzZnllAvENW-9ChFRPZBnsUgY18Y6HLWH-Wyf0V3_DE8kOxhtIHQdcKUVCQvb_a1TjuEsFMI6cdKmdOc8HLjSy7RfRAPmb7VT-6SDxz5mrMOEF5oGOF-M7RXHcWD_QFZjBmtaXRk0WnoeKgxFoDikLHCbTIxRwL92tyqwMx8QtpaW5JJ5wXtmy7EJ_jUl3SWpz_kEantNa-k9lV-iHn5E3rtd1KfxmYiGt7Y0uiMlrTy6Do7C5jZXiQ8Pk3WFCGh5nTIhU7nvSE4ZlflTK7QWJWw4vZ-_XDnFthHlQXb6IrIqrNvxvMYj3fUDXci6L1ExuNUSP6xwqQtPASGzTQYFr6XV3_WMhlnZeDVk4JwpEF7CTmRp524AO-W7bVPgp_fKIwD5TQJcMK9pB91ue3SDqMkSih-2YaHRxxVTSqqZ523cIqdCCUNs9BNw1sh38c",
    "expires_in": 3599,
    "token_type": "Bearer",
    "scope": [
        "categorization"
    ]
}
```

With access_token you can now call session creation - more about optional parameters and other options of api calls you can find on https://api.instacover.ai/.

```python
import requests
import json

url = "https://api.instacover.ai/instacar/v2.0/session/create"

payload = json.dumps({
  "callbackUrl": "**YOUR CALLBACK URL TO SEND FINISHED SESSION TO**",
  "expectedResults": { # optional - see more on https://api.instacover.ai/
    "odo": "",
    "vin": "",
    "model": "Octavia"
  },
  "steps": [
    "Vin",
    "VehicleRegistrationCertificateBack",
    "VehicleRegistrationCertificateFront",
    "RoadworthinessCertificateFront",
    "RoadworthinessCertificateBack"
  ],
  "optionalSteps": [
    "Vin",
    "VehicleRegistrationCertificateFront",
    "RoadworthinessCertificateFront"
  ],
  "forcedFilesystemPhotoUpload": False,
  "documentsFilesystemPhotoUpload": False,
  "redirectUrlOnSessionFinish": None,
  "extraPayloadData": {
    "caseId": "123456" # optional - see more on https://api.instacover.ai/
  }
})
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': 'Bearer **ACCESS_TOKEN**'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
# response example
{
    "link": "https://instacar.instacover.ai/clp9lr16i02lnr101u7kahdkjhasd",
    "sessionId": "clp9lr16i02lnr101u7kahdkjhasd",
    "expireAt": null
}
```