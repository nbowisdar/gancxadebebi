import json
import shutil

from config import RESULT_DIR


def main(drop_file_pages=False):
    full_data = []
    c = 1

    while True:
        try:
            with open(f"{RESULT_DIR}/page_{c}.json", "r", encoding="utf-8") as file:
                data = json.load(file)
            full_data.extend(data)
        except FileNotFoundError:
            break

        c += 1
        print(f"Collected {len(full_data)}, Page {c}")

    if drop_file_pages:
        shutil.rmtree(RESULT_DIR)
        RESULT_DIR.mkdir(exist_ok=True)

    with open(f"{RESULT_DIR}/full_data.json", "w", encoding="utf-8") as file:
        json.dump(full_data, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main(True)
