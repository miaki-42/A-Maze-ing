
gitignore
コーなケース
mypy(import)
README * 2


# subject見直し
- lint-strict (optional): Execute the commands flake8 . and mypy . --strict
- Include a .gitignore file to exclude Python artifacts.
- Outputfile:  All lines end with a \n 
```
You must provide a short documentation describing how to:
• Instantiate and use your generator, with at least a basic example.
• Pass custom parameters (e.g., size, seed).
• Access the generated structure, and access at least a solution.
```
- mazegenをrootに


# error
- 必須要素がない
- 不正な要素
- 重複要素
- イコールなし
- 空行
- 値が不正(たくさん)
- タプルがカンマでない
- 極端に小さい・大きいマップ
- seedありなし


tx = self.rng.randint(1, self.config.width - 2)
randint(1, 0) -> errorっぽい