import os
import pandas as pd
import re

def parse_line(line):
    try:
        timestamp = float(re.search(r'Timestamp:\s+([\d.]+)', line).group(1))
        can_id = re.search(r'ID:\s+([0-9a-fA-F]+)', line).group(1)
        dlc_match = re.search(r'DLC:\s+(\d+)', line)
        dlc = int(dlc_match.group(1)) if dlc_match else 0
        data = re.findall(r'([0-9a-fA-F]{2})', line.split('DLC:')[-1])
        data = data[:dlc] + ['00'] * (8 - dlc)  # Fill missing bytes
        return [timestamp, can_id, dlc] + data
    except:
        return None

def load_and_clean_txt(file_path):
    rows = []
    with open(file_path, 'r') as file:
        for line in file:
            parsed = parse_line(line)
            if parsed:
                rows.append(parsed)

    columns = ['Timestamp', 'CAN_ID', 'DLC'] + [f'DATA{i}' for i in range(8)]
    df = pd.DataFrame(rows, columns=columns)
    return df

def process_all_files(raw_dir, out_dir):
    for filename in os.listdir(raw_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(raw_dir, filename)
            df = load_and_clean_txt(file_path)
            df.to_csv(os.path.join(out_dir, filename.replace('.txt', '.csv')), index=False)
