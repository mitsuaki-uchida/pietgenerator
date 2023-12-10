"""
Pietプラグラム: コマンド配置器インタフェースモジュール
"""
import abc
import random
from enum import Enum
from typing import Any, NoReturn, TypeGuard

from pietgenerator.piet_common import Codel, Color, Command


class LayoutCommandError(Exception):
    """
    LayoutCommandErrorは、コマンドの配置に失敗した際に送出される例外である。
    """
    def __str__(self) -> str:
        """
        文字列表現

        Returns:
            str: 例外送出時のメッセージ
        """
        return f"{self.__class__.__name__}: layout command failed."


class LayoutCommand(Enum):
    """
    LayoutCommandは、コマンドを配置する際に使用する、Pietの仕様に存在しないコマンドである。

    Note:
        command_idは、piet_common.Command.command_idと重複しない。
    """

    ABORT = 200
    """ 停止用プログラムに配置されるコマンド """
    NOT_USE = 201
    """ Pietプログラムで未使用のgridに配置されるコマンド """

    def __init__(self, command_id: int) -> None:
        """
        インスタンス初期化

        Arguments:
            command_id (int): コマンドを示す一意のID
        """
        self._command_id = command_id

    def __str__(self) -> str:
        """
        文字列表現

        Returns:
            str: 自身の名前
        """
        return self.name


class ICommandLayouter(metaclass=abc.ABCMeta):
    """
    ICommandLayouterは、Pietプラグラムのコマンド配置器のインタフェースクラスである。
    コマンド配置器クラスは本クラスを継承し、未実装のインタフェースを定義すること。
    """

    def __init__(self, debug: bool, trace: bool) -> None:
        """
        インスタンス初期化

        デバッグオプションの設定

        Arguments:
            debug (bool): True: デバッグログ有効化; False: デバッグログ無効化
            trace (bool): True: トレースログ有効化; False: トレースログ無効化
        """
        self._debug = debug
        self._trace = trace

    def do_layout(self,
                  commands: list[Command],
                  start_color: Color,
                  abort_program_color: Color) -> list[list[Codel]]:
        """
        コマンド配置

        引数: commands で渡されたコマンドからCodelを生成し、生成したCodelを配置したgridを返却する。
        本メソッドは以下の責務を持つ。

        - gridのすべてのセルにCodelを配置すること。
        - 左上を原点(0, 0)とすること。
        - 原点に配置するCodelの色は、引数: start_color とすること。
        - gridに停止用プログラムを配置し、そのプログラムで自身を停止すること。
        - 停止用プログラムに配置するCodelの色は、引数: abort_program_color とすること。

        Arguments:
            commands (list[Command]): 配置するコマンドのリスト
            start_color (Color): 原点に配置するCodelの色
            abort_program_color (Color): 停止用プログラムに配置するCodelの色

        Returns:
            list[list[Codel]]: Codelを配置したgrid

        Raises:
            LayoutCommandError: コマンドの配置に失敗した
        """
        try:
            grid: list[list[Any]] = self._do_layout_impl(commands, start_color, abort_program_color)

            if not self._is_fill_all(grid):
                # Codelが配置されていないセルが存在する
                raise RuntimeError("has invalid cells.")

            return grid
        except Exception as e:
            raise LayoutCommandError() from e

    def _do_layout_impl(self,
                        commands: list[Command],
                        start_color: Color,
                        abort_program_color: Color) -> list[list[Any]] | NoReturn:
        """
        コマンド配置実装

        ICommandLayouter.do_layoutメソッドの実装を行う。
        本メソッドはインタフェースの宣言であるため、常にNotImplementedErrorを送出する。

        Arguments:
            commands (list[Command]): 配置するコマンドのリスト
            start_color (Color): 原点に配置するCodelの色
            abort_program_color (Color): 停止用プログラムに配置するCodelの色

        Raises:
            NotImplementedError: 本メソッドを呼び出した場合
        """
        raise NotImplementedError

    @staticmethod
    def _is_fill_all(grid: list[list[Any]]) -> TypeGuard[list[list[Codel]]]:
        """
        全セルCodel配置済み判定

        引数: grid のすべてのセルにCodelが配置されているか判定する。

        Arguments:
            grid (list[list[Any]]): 判定するgrid

        Returns:
            bool: すべてのセルにCodelが配置されている場合はTrue

        Note:
            本メソッドはTypeGuardであるため、本メソッド実行後は引数: grid の
            すべてのセルにCodelが配置されていることを保証する。
        """
        for row in grid:
            for codel in row:
                if not isinstance(codel, Codel):
                    # Codelではない
                    return False

        return True

    @staticmethod
    def _is_conflict(color: Color, grid: list[list[None | Codel]], x: int, y: int) -> bool:
        """
        競合判定

        引数: x / y で与えられた座標に引数: color を配置した場合、引数: grid 上で
        競合が発生するか判定する。
        ここで、競合の発生とは隣接する配置済みのCodelが保持するColorと同一色の
        Codelの配置を行うことを指す。
        ただし、白色 (Color.WHITE)、および黒色 (Color.BLACK)は競合の対象外とする。

        Arguments:
            color (Color): 競合判定を行う色
            grid (list[list[None | Codel]]): grid
            x (int): 競合判定を行うx座標
            y (int): 競合判定を行うy座標

        Returns:
            bool: 競合が発生した場合はTrue
        """
        if (color is Color.WHITE) or (color is Color.BLACK):
            # 競合判定対象外
            return False

        h: int = len(grid)
        w: int = len(grid[0])

        # 隣接するセルの色を取得する内部関数
        def _get_color_from_codel(codel: None | Codel) -> None | Color:
            if codel:
                return codel.color
            return None

        left_color: None | Color = None if x == 0 else _get_color_from_codel(grid[y][x - 1])
        upper_color: None | Color = None if y == 0 else _get_color_from_codel(grid[y - 1][x])
        right_color: None | Color = None if x == (w - 1) else _get_color_from_codel(grid[y][x + 1])
        under_color: None | Color = None if y == (h - 1) else _get_color_from_codel(grid[y + 1][x])

        # 競合判定
        return color in {upper_color, under_color, left_color, right_color}

    @staticmethod
    def _get_random_color(exclude_colors: list[Color] | None = None) -> Color | NoReturn:
        """
        任意の色取得

        引数: exclude_colors に含まれない、色相 / 明度を持つ任意の色を取得する。

        Arguments:
            exclude_colors (list[Color], optional): 除外する色

        Returns:
            Color: 任意の色

        Raises:
            RuntimeError: すべての色が除外された場合
        """
        colors: list[Color] = [
            Color.LIGHT_RED,
            Color.LIGHT_YELLOW,
            Color.LIGHT_GREEN,
            Color.LIGHT_CYAN,
            Color.LIGHT_BLUE,
            Color.LIGHT_MAGENTA,
            Color.RED,
            Color.YELLOW,
            Color.GREEN,
            Color.CYAN,
            Color.BLUE,
            Color.MAGENTA,
            Color.DARK_RED,
            Color.DARK_YELLOW,
            Color.DARK_GREEN,
            Color.DARK_CYAN,
            Color.DARK_BLUE,
            Color.DARK_MAGENTA
        ]

        if exclude_colors:
            for exclude_color in exclude_colors:
                colors.remove(exclude_color)

        if not colors:
            # すべての色が除外された
            raise RuntimeError("No color left.")

        return random.choice(colors)

    @staticmethod
    def _get_random_command(exclude_commands: list[Command] | None = None) -> Command | NoReturn:
        """
        任意のコマンド取得

        引数: exclude_commands に含まれない任意のコマンドを取得する。
        ただし、以下のコマンドは返却しない。

        - NONEコマンド: 連続した色のCodelが配置される。
        - SWITCHコマンド / POINTERコマンド: プログラムの実行方向が変更される。
        - IN_NUMBER / IN_CHARコマンド: プログラムが標準入力を待ってしまう。
        - OUT_NUMBER / OUT_CHARコマンド: プログラムの出力が変更されてしまう。
        - ROLLコマンド: メッセージ出力用コマンドの順序が変更される可能性がある。

        Arguments:
            exclude_commands (list[Command], optional): 除外するコマンド

        Returns:
            Command: 任意のコマンド

        Raises:
            RuntimeError: すべてのコマンドが除外された場合
        """
        commands: list[Command] = [
            # Command.NONE,
            Command.PUSH,
            Command.POP,
            Command.ADD,
            Command.SUBTRACT,
            Command.MULTIPLY,
            Command.DIVIDE,
            Command.MOD,
            Command.NOT,
            Command.GREATER,
            # Command.POINTER,
            # Command.SWITCH,
            Command.DUPLICATE,
            # Command.ROLL,
            # Command.IN_NUMBER,
            # Command.IN_CHAR,
            # Command.OUT_NUMBER,
            # Command.OUT_CHAR,
        ]

        if exclude_commands:
            for exclude_command in exclude_commands:
                commands.remove(exclude_command)

        if not commands:
            # すべてのコマンドが除外された
            raise RuntimeError("No command left.")

        return random.choice(commands)
