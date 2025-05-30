# Laboratory Work 2: Merge two JSON files

## Task Description

Merge two provided JSON files (`users1.json` and `users2.json`) into a single JSON file (`users.json`) using Python.
- Read `users1.json` file using Python.
- Read `users2.json` file using Python.
- Merge `users1.json` data with `users2.json` data.
- Save the merged data to `users.json`.

## Python Code

```python
import json

# Define file paths
file1_path = 'users1.json'
file2_path = 'users2.json'
merged_file_path = 'users.json'

# Read users1.json
try:
    with open(file1_path, 'r') as f1:
        data1 = json.load(f1)
    print(f"Successfully read {file1_path}")
except FileNotFoundError:
    print(f"Error: {file1_path} not found.")
    data1 = {"table": {"users": {}}}
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {file1_path}.")
    data1 = {"table": {"users": {}}}

# Read users2.json
try:
    with open(file2_path, 'r') as f2:
        data2 = json.load(f2)
    print(f"Successfully read {file2_path}")
except FileNotFoundError:
    print(f"Error: {file2_path} not found.")
    data2 = {"table": {"users": {}}}
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {file2_path}.")
    data2 = {"table": {"users": {}}}

# Merge data
merged_data = {"table": {"users": {}}}

if "table" in data1 and "users" in data1["table"]:
    merged_data["table"]["users"].update(data1["table"]["users"])

if "table" in data2 and "users" in data2["table"]:
    merged_data["table"]["users"].update(data2["table"]["users"])

# Save the merged data to users.json
try:
    with open(merged_file_path, 'w') as mf:
        json.dump(merged_data, mf, indent=4)
    print(f"Merged data saved to {merged_file_path}")
except IOError:
    print(f"Error: Could not write to {merged_file_path}.")

# Print the merged data
print("\nMerged JSON data:")
print(json.dumps(merged_data, indent=4))
```

## Input Files

### users1.json
```json
{
    "table": {
        "users": {
            "user1": {
                "name": "tester1",
                "codes": ["1", "2", "3", "4"],
                "surname": "tester1"
            },
            "user2": {
                "name": "tester2", 
                "codes": ["1", "2", "3", "4"],
                "surname": "tester2"
            }
        }
    }
}
```

### users2.json
```json
{
    "table": {
        "users": {
            "user3": {
                "name": "tester3",
                "codes": ["1", "2", "3", "4"],
                "surname": "tester3"
            }
        }
    }
}
```

## Expected Output

### users.json (merged result)
```json
{
    "table": {
        "users": {
            "user1": {
                "name": "tester1",
                "codes": ["1", "2", "3", "4"],
                "surname": "tester1"
            },
            "user2": {
                "name": "tester2",
                "codes": ["1", "2", "3", "4"], 
                "surname": "tester2"
            },
            "user3": {
                "name": "tester3",
                "codes": ["1", "2", "3", "4"],
                "surname": "tester3"
            }
        }
    }
}
```

## Report

The Python script demonstrates:
1. Reading JSON files with proper error handling for missing files and invalid JSON
2. Merging user dictionaries from both files under the "table" structure
3. Handling duplicate keys (values from the second file would overwrite the first)
4. Saving the combined data with proper formatting
5. Console output for verification

The merge operation successfully combines all users from both input files into a single JSON structure, maintaining the original nested format while adding all unique users to the merged result.
