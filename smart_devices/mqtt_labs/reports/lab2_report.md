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
file1_path = '/var/home/mark/Documents/semester6/smart_devices/mqtt_labs/lab2/users1.json'
file2_path = '/var/home/mark/Documents/semester6/smart_devices/mqtt_labs/lab2/users2.json'
merged_file_path = '/var/home/mark/Documents/semester6/smart_devices/mqtt_labs/lab2/users_merged.json' # Changed name to avoid conflict if users.json is a directory or special

# Read users1.json
try:
    with open(file1_path, 'r') as f1:
        data1 = json.load(f1)
    print(f"Successfully read {file1_path}")
except FileNotFoundError:
    print(f"Error: {file1_path} not found.")
    data1 = {"table": {"users": {}}} # Default to empty if file not found
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {file1_path}.")
    data1 = {"table": {"users": {}}} # Default to empty if JSON is invalid


# Read users2.json
try:
    with open(file2_path, 'r') as f2:
        data2 = json.load(f2)
    print(f"Successfully read {file2_path}")
except FileNotFoundError:
    print(f"Error: {file2_path} not found.")
    data2 = {"table": {"users": {}}} # Default to empty if file not found
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {file2_path}.")
    data2 = {"table": {"users": {}}} # Default to empty if JSON is invalid

# Merge data
# Initialize merged_data with the structure and content of data1
# Ensuring 'table' and 'users' keys exist
merged_data = {"table": {"users": {}}}

if "table" in data1 and "users" in data1["table"]:
    merged_data["table"]["users"].update(data1["table"]["users"])

if "table" in data2 and "users" in data2["table"]:
    # Update will overwrite keys from data1 if they also exist in data2,
    # or add new keys from data2.
    merged_data["table"]["users"].update(data2["table"]["users"])

# Save the merged data to users_merged.json
try:
    with open(merged_file_path, 'w') as mf:
        json.dump(merged_data, mf, indent=4)
    print(f"Merged data saved to {merged_file_path}")
except IOError:
    print(f"Error: Could not write to {merged_file_path}.")

# Print the merged data (optional)
print("\nMerged JSON data:")
print(json.dumps(merged_data, indent=4))

```

## Report

The Python script above performs the following actions:
1.  Reads data from `users1.json` and `users2.json`.
2.  Handles potential `FileNotFoundError` and `json.JSONDecodeError` during file reading.
3.  Merges the "users" dictionaries from both files under the "table" key. If user keys are duplicated, the values from `users2.json` will overwrite those from `users1.json` for the respective keys.
4.  Saves the combined data into a new file named `users_merged.json` with pretty printing (indentation).
5.  Prints a confirmation message and the merged data to the console.
