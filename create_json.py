import sys
import json
import os


def main():
    output_path, scan_id = sys.argv[1:3]
    viewpoint_ids = sys.argv[2:]

    with open(".tmp", "r") as f:
        viewpoint_ids = f.readline().split()

    if not os.path.exists(output_path):
        jsn = []
    else:
        with open(output_path, "r") as f:
            jsn = json.load(f)

    obj = {"scan_id": scan_id, "viewpoint_ids": viewpoint_ids}
    print(viewpoint_ids)
    jsn.append(obj)
    with open(output_path, "w") as f:
        output = json.dumps(jsn, indent=4)
        f.write(output)


if __name__ == "__main__":
    main()
