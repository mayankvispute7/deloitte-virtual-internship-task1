# import the necessary modules and libraries
import json, unittest, datetime

# load the json files
with open("./data-1.json","r") as f:
    jsonData1 = json.load(f)

with open("./data-2.json","r") as f:
    jsonData2 = json.load(f)

with open("./data-result.json","r") as f:
    jsonExpectedResult = json.load(f)


# convert json data from format 1 to the expected format
def convertFromFormat1(jsonObject):

    locationParts = jsonObject["location"].split("/")

    result = {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],
        "location": {
            "country": locationParts[0],
            "city": locationParts[1],
            "area": locationParts[2],
            "factory": locationParts[3],
            "section": locationParts[4]
        },
        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"]
        }
    }

    return result


# convert json data from format 2 to the expected format
def convertFromFormat2(jsonObject):

    # Convert ISO timestamp to milliseconds
    dt = datetime.datetime.fromisoformat(jsonObject["timestamp"].replace("Z", "+00:00"))
    timestamp = int(dt.timestamp() * 1000)

    result = {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": timestamp,
        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"]
        },
        "data": {
            "status": jsonObject["data"]["status"],
            "temperature": jsonObject["data"]["temperature"]
        }
    }

    return result


def main(jsonObject):

    if jsonObject.get("device") is None:
        return convertFromFormat1(jsonObject)
    else:
        return convertFromFormat2(jsonObject)


# Test cases
class TestSolution(unittest.TestCase):

    def test_sanity(self):
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult, "Type 1 conversion failed")

    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult, "Type 2 conversion failed")


if __name__ == "__main__":
    unittest.main()
