import json
import shutil

from config import RESULT_DIR


def inner(outer_c: int):
    full_data = []
    c = 1
    count = 0

    while True:
        try:
            with open(f"{RESULT_DIR / str(outer_c)}/page_{c}.json", "r", encoding="utf-8") as file:
                data = json.load(file)
            full_data.extend(data)
            count += len(data)
        except FileNotFoundError:
            print(f"Collected {len(full_data)}, From category {outer_c}")
            return full_data

        c += 1

    # with open(f"{RESULT_DIR}/full_data.json", "w", encoding="utf-8") as file:
    #     json.dump(full_data, file, indent=4, ensure_ascii=False)


def main():
    # c = 0
    full_data_all = []
    for i in range(1, 207):
        # c += inner(i)
        full_data_all.extend(inner(i))
    print(f"Collected {len(full_data_all)}")

    with open(f"{RESULT_DIR}/full_data_all.json", "w", encoding="utf-8") as file:
        json.dump(full_data_all, file, indent=4, ensure_ascii=False)


    print("All data collected", {"len": len(full_data_all)})
if __name__ == '__main__':
    main()
