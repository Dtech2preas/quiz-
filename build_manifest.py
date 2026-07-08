import os
import json
import hashlib
import time

def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def build_manifest():
    manifest = {
        "version": time.strftime("%Y.%m.%d.%H%M%S"),
        "minimumAppVersion": "1.0.0",
        "datasets": [],
        "assets": []
    }

    # Process Datasets
    dataset_dir = "dataset"
    if os.path.exists(dataset_dir):
        for root, _, files in os.walk(dataset_dir):
            for file in files:
                if file.endswith(".json") and file != "manifest.json":
                    filepath = os.path.join(root, file)

                    parts = filepath.split(os.sep)
                    grade = ""
                    subject = ""

                    # Examples: dataset/grade12/mathematics/paper1_algebra.json
                    # Or dataset/weekly_quiz/weekly_map.json
                    if len(parts) >= 4 and parts[1].startswith("grade"):
                        grade = parts[1]
                        subject = parts[2]
                    elif len(parts) >= 3 and parts[1] == "weekly_quiz":
                        subject = "weekly_quiz"

                    size = os.path.getsize(filepath)
                    file_hash = calculate_sha256(filepath)
                    web_path = "/" + filepath.replace(os.sep, "/")

                    manifest["datasets"].append({
                        "path": web_path,
                        "grade": grade,
                        "subject": subject,
                        "hash": file_hash,
                        "size": size,
                        "dependencies": []
                    })

    # We might also want map.json in datasets if it dictates the structure
    if os.path.exists("map.json"):
         size = os.path.getsize("map.json")
         file_hash = calculate_sha256("map.json")
         manifest["datasets"].append({
              "path": "/map.json",
              "grade": "",
              "subject": "map",
              "hash": file_hash,
              "size": size,
              "dependencies": []
         })

    with open("manifest.json", "w") as f:
        json.dump(manifest, f, indent=4)

    print(f"Successfully generated manifest.json with version {manifest['version']} containing {len(manifest['datasets'])} datasets.")

if __name__ == "__main__":
    build_manifest()
