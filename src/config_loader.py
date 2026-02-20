#!/usr/bin/env python3
"""
Loader for read the configuration file.
"""

from typing import Any


def load_config(file_path: str) -> dict[str, Any]:
    """
    Loads the configuration file.

    Args:
        file_path (str): Path to the configuration file.

    Returns:
        dict[str, Any]: Validated configuration data.

    Raises:
        Exception: If any error occurs during loading or parsing.
    """
    raw_data: dict[str, str] = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                if '=' not in line:
                    raise Exception(
                        f"Error: Invalid syntax at line {line_num}: '{line}'."
                    )

                key, value = line.split('=', 1)
                key = key.strip().upper()
                value = value.strip()

                if key in raw_data:
                    raise Exception(
                        f"Error: Duplicate key at line {line_num}: '{key}'."
                    )

                raw_data[key] = value

        formatted_data: dict[str, Any] = {
            "width": int(raw_data["WIDTH"]),
            "height": int(raw_data["HEIGHT"]),
            "entry": tuple(map(int, raw_data["ENTRY"].split(','))),
            "exit": tuple(map(int, raw_data["EXIT"].split(','))),
            "output_file": raw_data["OUTPUT_FILE"],
            "perfect": raw_data["PERFECT"],
        }

        if "SEED" in raw_data:
            formatted_data["seed"] = int(raw_data["SEED"])

        return formatted_data

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Error: Configuration file '{file_path}' not found."
        )
    except PermissionError:
        raise PermissionError(f"Error: Permission denied '{file_path}'")
    except KeyError as e:
        raise KeyError(f"Error: Missing mandatory configuration key: {e}")
    except ValueError as e:
        raise ValueError(f"Error: Invalid value in configuration: {e}")
    except Exception:
        raise
