# Laboratory Work 1: JSON Usage

## Task Description

Get a basic understanding of JSON by using it in the Python programming language. Modify the below given JSON example, using Python code:
- Change `firstName` and `lastName` to new values.
- Add a new entry called "Age" to the JSON example.

## Python Code

```python
import json

# Original JSON string
x = '{ "firstName": "tester", "lastName": "tester", "city": "Vilnius"}'
print(f"Original JSON string: {x}")

# Parse x:
y = json.loads(x)

# The result is a Python dictionary:
print(f"Original firstName: {y['firstName']}")

# Modify firstName and lastName
y["firstName"] = "John"
y["lastName"] = "Doe"

# Add new entry "Age"
y["Age"] = 30

# Print the modified Python dictionary
print(f"Modified Python dictionary: {y}")

# Convert the modified dictionary back to a JSON string
modified_json_string = json.dumps(y, indent=4)
print(f"Modified JSON string:\n{modified_json_string}")
```

## Report

The Python script above demonstrates the following:
1. Parsing a JSON string into a Python dictionary using `json.loads()`.
2. Modifying values for existing keys (`firstName`, `lastName`) in the dictionary.
3. Adding a new key-value pair (`Age`) to the dictionary.
4. Converting the modified Python dictionary back into a JSON string using `json.dumps()`, with indentation for readability.

## Output
When executed, the script produces:
```
Original JSON string: { "firstName": "tester", "lastName": "tester", "city": "Vilnius"}
Original firstName: tester
Modified Python dictionary: {'firstName': 'John', 'lastName': 'Doe', 'city': 'Vilnius', 'Age': 30}
Modified JSON string:
{
    "firstName": "John",
    "lastName": "Doe",
    "city": "Vilnius",
    "Age": 30
}
```
