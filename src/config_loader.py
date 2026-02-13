#!/usr/bin/env python3

import sys
from typing import Any
#from src.mazegen.models import MazeConfig

#def load_config(path: str) -> MazeConfig:
def load_config(file_path: str) -> dict[str, Any]:
    """
    設定ファイルを読み込み、バリデーション済みのMazeConfigオブジェクトを返します。

    Args:
        path (str): 設定ファイルへのパス

    Returns:
        MazeConfig: バリデーション済みの設定データ

    Raises:
        SystemExit: ファイル読み込みやパースに失敗した場合
    """
    raw_data: dict[str, str] = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                if '=' not in line:
                    print(f"Error: Invalid syntax at line {line_num}: "
                          f"'{line}'", file=sys.stderr)
                    sys.exit(1)

                key, value = line.split('=', 1)
                key = key.strip().upper()
                value = value.strip()

                if key in raw_data:
                    print(f"Error at line {line_num}: Duplicate key "
                          f"'{key}' found.", file=sys.stderr)
                    sys.exit(1)

                raw_data[key] = value

        formatted_data: dict[str, Any] = {
            "width": int(raw_data["WIDTH"]),
            "height": int(raw_data["HEIGHT"]),
            "entry": tuple(map(int, raw_data["ENTRY"].split(','))),
            "exit": tuple(map(int, raw_data["EXIT"].split(','))),
            "output_file": raw_data["OUTPUT_FILE"],
            "perfect": raw_data["PERFECT"].lower() == "true",
        }

        if "SEED" in raw_data:
            formatted_data["seed"] = int(raw_data["SEED"])

        return formatted_data
        #return MazeConfig(**formatted_data)

    except FileNotFoundError:
        print(f"Error: Configuration file '{path}' not found.",
              file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing mandatory configuration key: {e}",
              file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid value in configuration: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
