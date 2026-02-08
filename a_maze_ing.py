#!/usr/bin/env python3


if __name__ == "__main__":
    # ファイル読み取り


    # MazeGeneratorインスタンス作成


    # 迷路生成


    # 最短パス探索


    # ファイルに出力


    # mlxで描画


    # コマンド待機
    # 1.regenerate, 2.show & hide path, 3.rotate maze color, 4.exit


#class MazeGenerator:
#    """
#    ユーザーはこのクラスだけを操作する
#    """
#    def __init__(self, size=(20, 20), perfect=True):
#        self.size = size
#        # 内部で役割を分担
#        self._strategy = RecursiveBacktracker(size, perfect)
#        self._solver = BreadthFirstSearch()
#        self._maze_data = None

#    def generate(self, seed=0):
#        # 生成ロジックに委譲
#        self._maze_data = self._strategy.create(seed)

#    @property
#    def shortest_path(self):
#        # 探索ロジックに委譲
#        return self._solver.find_path(self._maze_data)

#    def save(self, filename):
#        # ファイル出力ロジック
#        FileHandler.save(self._maze_data, filename)


