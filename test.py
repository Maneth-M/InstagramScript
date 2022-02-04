import json
import datetime
X = json.dumps({f"{datetime.datetime.now()}": 30})
print(X)