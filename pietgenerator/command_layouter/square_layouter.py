"""
Pietプラグラム: コマンド配置器モジュール (正方形)
"""
import math
from typing import Any, Callable, NoReturn

from pietgenerator.piet_common import Codel, Color, Command, DirectionPointer
from pietgenerator.piet_common import get_command_from_color, get_color_from_command
from pietgenerator.command_layouter.command_layouter import (ICommandLayouter,
                                                             LayoutCommand,
                                                             LayoutCommandError)


class GridTooSmallError(LayoutCommandError):
    """
    GridTooSmallErrorは、コマンドの配置中にgrid内のセルが不足した際に送出される例外である。
    本例外はモジュール内で補足し、モジュール外に送出しない。
    """

    def __init__(self, w: int, h: int, x: int, y: int) -> None:
        """
        インスタンス初期化

        Arguments:
            w (int): gridの幅
            h (int): gridの高さ
            x (int): 例外送出時のx座標
            y (int): 例外送出時のy座標
        """
        self._w = w
        self._h = h
        self._x = x
        self._y = y

    def __str__(self) -> str:
        """
        文字列表現

        Returns:
            str: 例外送出時のメッセージ
        """
        return (f"{self.__class__.__name__}: grid is too small. "
                f"w={self._w} h={self._h} pos=({self._x}, {self._y})")


class SquareLayouter(ICommandLayouter):
    """
    SquareLayouterは、Pietプラグラムのコマンド(LayoutCodel)を正方形に配置するクラスである。
    SquareLayouterは、以下のようにコマンドの配置を行う。

    - 左上を原点(0, 0)とした正方形のgridにコマンドを配置する。
    - gridの中央に停止用プログラムを配置する。
    - 原点から停止用プログラムまで時計回りの螺旋状にコマンドを配置する。
    """

    # pylint: disable=line-too-long
    _ABORT_PROGRAM_ODD: list[list[None | Command | LayoutCommand]] = [
        [None, None,         Command.EDGE,        None,                None],           # noqa: E241,E501
        [None, Command.EDGE, LayoutCommand.ABORT, Command.EDGE,        None],           # noqa: E241,E501
        [None, None,         LayoutCommand.ABORT, LayoutCommand.ABORT, Command.EDGE],   # noqa: E241,E501
        [None, Command.EDGE, LayoutCommand.ABORT, Command.EDGE,        None],           # noqa: E241,E501
        [None, None,         Command.EDGE,        None,                None],           # noqa: E241,E501
    ]
    """ 停止用プログラム (奇数プログラムgrid用) """

    # pylint: disable=line-too-long
    _ABORT_PROGRAM_EVEN: list[list[None | Command | LayoutCommand]] = [
        [None, None,         Command.EDGE,        Command.EDGE,        None,                None],          # noqa: E241,E501
        [None, Command.EDGE, LayoutCommand.ABORT, LayoutCommand.ABORT, Command.EDGE,        None],          # noqa: E241,E501
        [None, None,         LayoutCommand.ABORT, LayoutCommand.ABORT, LayoutCommand.ABORT, Command.EDGE],  # noqa: E241,E501
        [None, None,         LayoutCommand.ABORT, LayoutCommand.ABORT, LayoutCommand.ABORT, Command.EDGE],  # noqa: E241,E501
        [None, Command.EDGE, LayoutCommand.ABORT, LayoutCommand.ABORT, Command.EDGE,        None],          # noqa: E241,E501
        [None, None,         Command.EDGE,        Command.EDGE,        None,                None],          # noqa: E241,E501
    ]
    """ 停止用プログラム (偶数プログラム(grid)用) """

    def __init__(self, debug: bool = True, trace: bool = False) -> None:
        """
        インスタンス初期化

        デバッグオプションの設定

        Arguments:
            debug (bool): True: デバッグログ有効化; False: デバッグログ無効化
            trace (bool): True: トレースログ有効化; False: トレースログ無効化
        """
        super().__init__(debug, trace)

    def _do_layout_impl(self,
                        commands: list[Command],
                        start_color: Color,
                        abort_program_color: Color) -> list[list[Any]] | NoReturn:
        """
        メッセージ -> コマンド生成実装

        ICommandGenerator.generateメソッドの実装を行う。

        Arguments:
            commands (list[Command]): 配置するコマンドのリスト
            start_color (Color): 原点に配置するCodelの色
            abort_program_color (Color): 停止用プログラムに配置するCodelの色

        Returns:
            list[list[Any]]: Codelを配置したgrid

        Raises:
            LayoutCommandError: コマンドの配置に失敗した
        """
        # 試行回数を少なくするため、メッセージ出力用コマンドのコマンド数からgridサイズを予測する
        w, h = self._predict_grid_size(commands)

        while True:
            # Pietプログラム開始位置 / DP / 色
            # Pietプログラム開始位置は、Pietの仕様で"左上"(原点(0, 0))と定められている
            # DPの初期値は、Pietの仕様で"右"と定められている
            x = 0
            y = 0
            dp = DirectionPointer.RIGHT
            color = start_color

            # grid生成
            grid: list[list[Codel | None]] = self._create_grid(w, h, abort_program_color)

            try:
                # メッセージ出力用コマンドをgridに螺旋状に配置する
                x, y, dp, color = self._put_codels(commands, grid, x, y, dp, color)

                # 停止用プログラムまで移動するコマンドをgridに配置する
                x, y, dp, color = self._put_codels_to_abort_area(commands, grid, x, y, dp, color)
                x, y, dp, color = self._put_codels_to_abort_program(abort_program_color,
                                                                    grid, x, y, dp, color)

                # grid上の未使用のLayoutCodelに任意のコマンド(色)を配置する
                self._put_to_empty_cells(grid)

                break
            except GridTooSmallError as e:
                # gridにコマンドが配置しきれなかった
                if self._debug:
                    print(e)
                    self._dump_grid(grid)

                # gridを拡大してリトライ
                w += 1
                h += 1

        if self._debug:
            print("do_layout_impl: exit. "
                  f"pos=({x}, {y}) dp={str(dp)} color={color}")
            self._dump_grid(grid)

        return grid

    def _predict_grid_size(self, commands: list[Command]) -> tuple[int, int]:
        """
        gridサイズ予測

        引数: commands で渡されたコマンドの配置に必要なgridのサイズを予測する。

        Arguments:
            commands (list[Command]): 配置するコマンドのリスト

        Returns:
            (int, int): gridの予測幅 / gridの予測高さ
        """
        command_num = len(commands)

        # 追加する回転用コマンドの予測数
        # = メッセージ出力用コマンドを正方形に螺旋状に配置した場合の周回数 * 1周に使用する回転用コマンド数
        # = (正方形の一辺の長さ / 2) * (4 * (PUSHコマンド + POINTERコマンド))
        # = (sqrt(コマンド数) / 2) * (4 * 2)
        # = sqrt(コマンド数) * 4
        predict_rotete_num = int(math.ceil(math.sqrt(command_num))) * 4

        # 停止用プログラムのサイズ
        abort_program_w = len(self._ABORT_PROGRAM_ODD[0])
        abort_program_h = len(self._ABORT_PROGRAM_ODD)

        # コマンドの予測数
        # = メッセージ出力用コマンド数 + 回転用コマンド予測数 + 停止用プログラムのコマンド数
        predict_commands_num = (command_num +
                                predict_rotete_num +
                                (abort_program_w * abort_program_h))

        # グリッドの幅、高さ
        # = 予測したコマンドをすべて配置した正方形の一辺の長さ
        # = sqrt(予測したコマンド数)
        w = int(math.ceil(math.sqrt(predict_commands_num)))
        h = w

        # 最小でも停止用プログラムを一周できるサイズに補正
        w = max(w, abort_program_w + 2)
        h = max(h, abort_program_h + 2)

        if self._debug:
            print("predict_grid_size: exit. "
                  f"command_num={command_num} "
                  f"predict_command_num={predict_commands_num} w={w} h={h}")

        return w, h

    def _create_grid(self, w: int, h: int, abort_program_color: Color) -> list[list[None | Codel]]:
        """
        grid生成

        引数: w / h で渡されたサイズのgridを生成する。
        生成したgridの中央のセルには、引数: abort_program_color で指定した色で
        停止用プログラムが配置されており、それ以外のセルにはNoneが配置されている。

        Arguments:
            w (int): gridの幅
            h (int): gridの高さ
            abort_program_color (Color): 停止用プログラムに配置するCodelの色

        Returns:
            list[list[None | Codel]]: grid
        """
        grid: list[list[None | Codel]] = [[None] * w for _ in range(h)]

        # gridのサイズから停止用プログラムを取得
        abort_program = self._get_abort_program(w, h)
        abort_program_h = len(abort_program)
        abort_program_w = len(abort_program[0])

        # 停止用プログラムの配置位置(原点からのオフセット量)を算出
        offset_x = (w // 2) - (abort_program_w // 2)
        offset_y = (h // 2) - (abort_program_h // 2)

        # 停止用プログラムを配置
        for y in range(abort_program_h):
            for x in range(abort_program_w):
                command = abort_program[y][x]
                if command is Command.EDGE:
                    grid[y + offset_y][x + offset_x] = Codel(Color.BLACK)
                elif command is LayoutCommand.ABORT:
                    grid[y + offset_y][x + offset_x] = Codel(abort_program_color)

        return grid

    def _get_abort_program(self, w: int, _: int) -> list[list[None | Command | LayoutCommand]]:
        """
        停止用プログラム取得

        gridのサイズに適した停止用プログラムを取得する。
        現状の仕様ではgridは正方形であるため、gridの幅のみ使用する。

        Arguments:
            w (int): gridの幅
            h (int): gridの高さ (未使用のため '_')

        Returns:
            list[list[Command | LayoutCommand]]: 停止用プログラムのコマンドが配置されたgrid
        """
        return self._ABORT_PROGRAM_EVEN if (w % 2) == 0 else self._ABORT_PROGRAM_ODD

    def _is_in_abort_program_area(self, grid: list[list[None | Codel]], x: int, y: int) -> bool:
        """
        停止用プログラム領域侵入判定

        引数: x / y で与えられた座標が引数: grid に配置された停止用プログラムの
        領域内であるかを判定する。
        停止用プログラムに隣接する左側一列も、停止用プログラムへの移動領域として使用するため、
        停止用プログラムの領域内であると判定する。

        Arguments:
            grid (list[list[None | Codel]]): grid
            x (int): x座標
            y (int): y座標

        Returns:
            bool: 停止用プログラムの領域内である場合はTrue
        """
        # 停止用プログラムの領域の最大 / 最小インデックスを算出
        h: int = len(grid)
        w: int = len(grid[0])

        abort_program: list[list[None | Command | LayoutCommand]] = self._get_abort_program(w, h)
        abort_program_h: int = len(abort_program)
        abort_program_w: int = len(abort_program[0])

        min_x: int = (w // 2) - (abort_program_w // 2)
        min_y: int = (h // 2) - (abort_program_h // 2)
        max_x: int = min_x + abort_program_w
        max_y: int = min_y + abort_program_h

        # 停止用プログラムへの移動領域分、インデックスを補正
        min_x -= 1

        return ((min_x <= x < max_x) and (min_y <= y < max_y))

    def _put_codels(self,
                    commands: list[Command],
                    grid: list[list[None | Codel]],
                    x: int,
                    y: int,
                    dp: DirectionPointer,
                    color: Color) -> tuple[int, int, DirectionPointer, Color]:
        """
        Codel配置

        引数: commands で与えられたコマンドからCodelを生成し、引数: grid に配置する。
        gridへの配置は引数: x / y / dp / color の各値を初期値として開始し、
        配置が正常に完了した場合は、配置後の x / y / dp / color を返却する。
        Codelの配置中に停止用プログラムの領域に到達した場合は、GridTooSmallErrorを送出する。

        Arguments:
            commands (list[Command]): 配置するコマンドのリスト
            grid (list[list[None | Codel]]): Codelの配置を行うgrid
            x (int): 配置開始時のx座標
            y (int): 配置開始時のy座標
            dp (DirectionPointer): 配置開始時のDP
            color (Color): 配置開始時の色

        Returns:
            (int, int, DirectionPointer, Color): 配置完了時のx座標 / y座標 / DP / 色

        Raises:
            GridTooSmallError: コマンドの配置中に停止用プログラムの領域に到達した
        """
        h: int = len(grid)
        w: int = len(grid[0])
        command_index: int = 0

        # すべてのコマンドの配置が完了するまで実行
        while command_index < len(commands):
            if self._is_in_abort_program_area(grid, x, y):
                # コマンドがgridに配置しきれなかった
                raise GridTooSmallError(w, h, x, y)

            # 1ライン分のCodelを配置
            command_index, x, y, dp, color = self._put_codels_on_line(commands, command_index,
                                                                      grid, x, y, dp, color)

        if self._debug:
            print("put_codels: exit. "
                  f"pos=({x}, {y}) dp={str(dp)} color={color}")

        return x, y, dp, color

    def _put_codels_to_abort_area(self,
                                  commands: list[Command],
                                  grid: list[list[None | Codel]],
                                  x: int,
                                  y: int,
                                  dp: DirectionPointer,
                                  color: Color) -> tuple[int, int, DirectionPointer, Color]:
        """
        停止用プログラム領域端までのCodel配置

        引数: x / y / dp / color の各値を初期値(開始地点)として、その地点から
        停止用プログラム領域端まで任意のCodelを配置する。
        配置が正常に完了した場合は、配置後の x / y / dp / color を返却する。

        本メソッドでCodelの配置を行う際、競合により配置済みのCodelを
        再配置することがある(※1)。
        停止用プログラム領域端への移動が完了した時点で、Codelの再配置が
        行われていない場合は、GridTooSmallErrorを送出する。

        ※1: 開始地点の2セル先にPUSHコマンド / POINTERコマンドを配置する際に競合が発生した場合

        Arguments:
            commands (list[Command]): 配置済みコマンドのリスト
            grid (list[list[None | Codel]]): Codelを配置するgrid
            x (int): 移動開始時のx座標
            y (int): 移動開始時のy座標
            dp (DirectionPointer): 移動開始時のDP
            color (Color): 移動開始時の色

        Returns:
            (int, int, DirectionPointer, Color): 移動完了時のx座標 / y座標 / DP / 色

        Raises:
            GridTooSmallError: Codelの再配置が未完了である
        """
        # 開始地点より前に配置したコマンドのコマンド数を保存
        original_command_length: int = len(commands)
        command_index: int = original_command_length

        while True:
            if self._is_in_abort_program_area(grid, x, y):
                # 停止用プログラムまで到達した

                if command_index < original_command_length:
                    # 再配置が必要なコマンドの再配置が行われていない
                    raise GridTooSmallError(len(grid[0]), len(grid), x, y)

                # 配置完了
                break

            if command_index >= len(commands):
                # 配置するコマンドが不足した場合は、末尾に不足数分の任意のコマンドを追加する
                need_command_num = command_index - len(commands) + 1
                commands += [self._get_random_command() for _ in range(need_command_num)]

            # 1ライン分のコマンドを配置
            command_index, x, y, dp, color = self._put_codels_on_line(commands, command_index,
                                                                      grid, x, y, dp, color)

        if self._debug:
            print("put_codels_to_abort_area: exit. "
                  f"pos=({x}, {y}) dp={str(dp)} color={color}")

        return x, y, dp, color

    def _put_codels_to_abort_program(self,
                                     abort_program_color: Color,
                                     grid: list[list[None | Codel]],
                                     x: int,
                                     y: int,
                                     dp: DirectionPointer,
                                     color: Color) -> tuple[int, int, DirectionPointer, Color]:
        """
        停止用プログラム開始位置までのCodel配置

        引数: x / y / dp / color の各値を停止用プログラム領域端地点での値として、
        その地点から停止用プログラム開始位置まで任意のCodelを配置する。
        配置が完了した場合は、移動後の x / y / dp / color を返却する。

        具体的には、以下のX1からX5までのCodelを配置する。
        また、引数: x / y / dp / colorはX1のセルとなり、移動後の x / y / dp / colorはX5に隣接する
        Aのセルとなる。

        ::

            gridが奇数での配置       gridが偶数での配置
            +--+--+--+--+--+--+     +--+--+--+--+--+--+--+
            |  |  |  |  |  |  |     |  |  |  |E |E |  |  |
            +--+--+--+--+--+--+     +--+--+--+--+--+--+--+
            |  |  |  |E |  |  |     |  |  |E |A |A |E |  |
            +--+--+--+--+--+--+     +--+--+--+--+--+--+--+
            |  |  |E |A |E |  |     |  |  |  |A |A |A |E |
            +--+--+--+--+--+--+     +--+--+--+--+--+--+--+
            |X3|X4|X5|A |A |E |     |X3|X4|X5|A |A |A |E |
            +--+--+--+--+--+--+     +--+--+--+--+--+--+--+
            |X2|  |E |A |E |  |     |X2|  |E |A |A |E |  |
            +--+--+--+--+--+--+     +--+--+--+--+--+--+--+
            |X1|  |  |E |  |  |     |X1|  |  |E |E |  |  |
            +--+--+--+--+--+--+     +--+--+--+--+--+--+--+
            |C |  |  |  |  |  |     |C |  |  |  |  |  |  |
            +--+--+--+--+--+--+     +--+--+--+--+--+--+--+

            C:     移動元のセル
                   x / y / dpは次の異動先となるX1のセルを指す
            X1-X5: 本メソッドでCodelの配置を行うセル
                   X2はPUSHコマンド、X3はPOINTERコマンドを配置し、それ以外は任意のコマンドを配置する
                   ただし、X5 -> A移動時に実行すると問題のあるコマンドは配置しない
            A:     停止用プログラムのABORTコマンドが配置されたセル
            E:     停止用プログラムのEDGEコマンドが配置されたセル

        Arguments:
            grid (list[list[LayoutCodel]]): 移動を行うgrid
            x (int): 移動開始時のx座標
            y (int): 移動開始時のy座標
            dp (DirectionPointer): 移動開始時のDP
            color (Color): 移動開始時の色

        Returns:
            (int, int, DirectionPointer, Color): 移動完了時のx座標 / y座標 / DP / 色
        """
        # 3セル直進し、右に曲がる
        exclude_commands: list[Command] = []

        while True:
            # 1セル目: 任意のコマンド
            random_command: Command = self._get_random_command(exclude_commands)
            random_color: Color = get_color_from_command(random_command, color)
            # 2セル目: PUSHコマンド
            push_color: Color = get_color_from_command(Command.PUSH, random_color)
            # 3セル目: POINTERコマンド
            pointer_color: Color = get_color_from_command(Command.POINTER, push_color)

            if (self._is_conflict(random_color, grid, x + (dp.dx * 0), y + (dp.dy * 0)) or
                self._is_conflict(push_color, grid, x + (dp.dx * 1), y + (dp.dy * 1)) or
                self._is_conflict(pointer_color, grid, x + (dp.dx * 2), y + (dp.dy * 2))):
                # 色の競合が発生した場合はリトライ
                exclude_commands.append(random_command)
                continue

            # 競合が発生しない色でコマンドが確定したのでgridに配置し、x / y / dp / colorを更新
            for (command_, color_) in [(random_command, random_color),
                                       (Command.PUSH, push_color),
                                       (Command.POINTER, pointer_color)]:
                grid[y][x] = Codel(color_)

                if self._trace:
                    print("put_codels_to_abort_program: "
                          f"pos=({x}, {y}) command_index=--- "
                          f"command={command_} color={color_}")

                if command_ is Command.POINTER:
                    dp = DirectionPointer.rotate(dp, 1)

                color = color_
                x += dp.dx
                y += dp.dy

            # 配置完了
            break

        # 2セル直進する
        exclude_commands1: list[Command] = []
        exclude_commands2: list[Command] = []
        while True:
            # 1セル目: 任意のコマンド
            random_command1: Command = self._get_random_command(exclude_commands1)
            random_color1: Color = get_color_from_command(random_command1, color)

            if self._is_conflict(random_color1, grid, x + (dp.dx * 0), y + (dp.dy * 0)):
                # 色の競合が発生した場合はリトライ
                exclude_commands1.append(random_command1)
                continue

            # 2セル目: 任意のコマンド
            random_command2: Command = self._get_random_command(exclude_commands2)
            random_color2: Color = get_color_from_command(random_command2, random_color1)

            if self._is_conflict(random_color2, grid, x + (dp.dx * 1), y + (dp.dy * 1)):
                # 色の競合が発生した場合はリトライ
                exclude_commands2.append(random_command2)
                continue

            if get_command_from_color(random_color2, abort_program_color) in [
                Command.IN_CHAR,
                Command.IN_NUMBER,
                Command.OUT_CHAR,
                Command.OUT_NUMBER,
            ]:
                # 停止用プログラムがコマンドとして実行された際に、
                # IN / OUTコマンドとして実行される場合はリトライ
                exclude_commands2.append(random_command2)
                continue

            # 競合が発生しない色でコマンドが確定したのでgridに配置し、x / y / dp / colorを更新
            for (command_, color_) in [(random_command1, random_color1),
                                       (random_command2, random_color2)]:
                grid[y][x] = Codel(color_)

                if self._trace:
                    print("put_codels_to_abort_program: "
                          f"pos=({x}, {y}) command_index=--- "
                          f"command={command_} color={color_}")

                if command_ is Command.POINTER:
                    dp = DirectionPointer.rotate(dp, 1)

                color = color_
                x += dp.dx
                y += dp.dy

            # 配置完了
            break

        if self._debug:
            print("put_codels_to_abort_program: exit. "
                  f"pos=({x}, {y}) dp={str(dp)} color={color}")

        return x, y, dp, color

    def _put_codels_on_line(self,
                            commands: list[Command],
                            command_index: int,
                            grid: list[list[None | Codel]],
                            x: int,
                            y: int,
                            dp: DirectionPointer,
                            color: Color) -> tuple[int, int, int, DirectionPointer, Color]:
        """
        Codel配置(1ライン)

        引数: commands で与えられたコマンドから生成したCodelを縦方向、または横方向の
        1ライン分、引数: grid に配置する。
        gridへの配置は引数: x / y / dp / color の各値を初期値として開始し、
        1ライン分の配置が完了した場合、またはコマンド末尾まで配置が完了した場合は、
        配置後の x / y / dp / color を返却する。

        Arguments:
            commands (list[Command]): 配置するコマンドのリスト
            command_index (int): 配置開始時のcommandsのindex
            grid (list[list[None | Codel]]): Codelを配置するgrid
            x (int): 配置開始時のx座標
            y (int): 配置開始時のy座標
            dp (DirectionPointer): 配置開始時のDP
            color (Color): 配置開始時のColor

        Returns:
            (int, int, int, DirectionPointer, Color):
                配置完了時のcommandsのindex / x座標 / y座標 / DP / 色
        """

        def _conflict_resolver() -> Callable[[int], None]:
            """
            競合解決用Closure

            本関数内で行われる競合解決処理を纏めたClosureである。

            Returns:
                Callable[[int], None]: 競合解決用関数
            """
            last_free_x: int = -1
            last_free_y: int = -1
            exclude_colors: list[Color] = []
            last_resolve_color: Color = Color.BLACK

            def _resolve_conflict(relocate_command_num: int) -> None:
                """
                競合解決用関数

                本Closureで返却される競合解決用の関数である。
                参照 / 更新する変数が多岐に渡るため nonlocal を措定して共有する。

                Arguments:
                    relocate_command_num (int): 競合解決時に再配置が必要なコマンド数
                """
                nonlocal last_free_x, last_free_y, exclude_colors, last_resolve_color
                nonlocal grid, x, y, command_index, dp, color

                if self._debug:
                    print("resolve_conflict: conflict occurred. "
                          f"pos=({x}, {y}) command_index={command_index} "
                          f"relocate_command_num={relocate_command_num} "
                          f"last_free_pos=({last_free_x}, {last_free_y})")

                if (last_free_x + last_free_y) < 0:
                    # 再配置が必要なコマンド数分だけ、commnadsのindex、および x / y 座標を戻す
                    command_index -= relocate_command_num
                    x -= (dp.dx * relocate_command_num)
                    y -= (dp.dy * relocate_command_num)

                    # FREE_ZONEコマンドを配置し、配置したx / y座標を保存する
                    grid[y][x] = Codel(Color.WHITE)
                    last_free_x = x
                    last_free_y = y

                    if self._trace:
                        print("resolve_conflict: "
                              f"pos=({x}, {y}) command_index=--- "
                              f"command={Command.FREE_ZONE} color={Color.WHITE}")

                    x += dp.dx
                    y += dp.dy
                else:
                    # 以前に配置したFREE_ZONEコマンドまで、commnadsのindex、および x / y 座標を戻す
                    # 末尾の + 2 は、FREE_ZONEコマンド / NONEコマンドの追加分を除外するため
                    command_index += -max(abs(x - last_free_x), abs(y - last_free_y)) + 2
                    x = last_free_x + dp.dx
                    y = last_free_y + dp.dy

                resolve_color: Color = Color.BLACK
                while True:
                    # 競合の解決に使用する色を取得
                    try:
                        resolve_color = self._get_random_color(exclude_colors)
                    except RuntimeError as e:
                        # 競合の解決に使用可能な色が枯渇
                        # (last_free_x, last_free_y)では、以降に発生するすべての競合を解決できなかった
                        if self._debug:
                            print(e)

                        # 最後にconflictの解決に使用した色で(last_free_x, last_free_y)での
                        # 競合を解決し、次の箇所で改めてconflictの解決を行う
                        resolve_color = last_resolve_color
                        last_free_x = -1
                        last_free_y = -1
                        exclude_colors.clear()
                        break

                    if self._is_conflict(resolve_color, grid, x, y):
                        exclude_colors.append(resolve_color)
                        continue

                    # 競合の解決に使用する色が決定した

                    # 使用する色はlast_resolve_colorに保存する
                    last_resolve_color = resolve_color
                    exclude_colors.append(resolve_color)
                    break

                grid[y][x] = Codel(resolve_color)

                if self._trace:
                    print("resolve_conflict: "
                          f"pos=({x}, {y}) command_index=--- "
                          f"command={Command.NONE} color={resolve_color}")

                x += dp.dx
                y += dp.dy
                color = resolve_color

                if self._debug:
                    print("resolve_conflict: conflict resolved. "
                          f"pos=({x}, {y}) command_index={command_index} color={resolve_color} "
                          "exclude_colors="
                          f"{[str(exclude_color) for exclude_color in exclude_colors]}")

            return _resolve_conflict

        resolve_conflict: Callable = _conflict_resolver()
        start_x: int = x
        start_y: int = y

        w: int = len(grid[0])
        h: int = len(grid)
        length: int = 0

        # x / y座標、およびDPの方向から、配置するコマンドの長さを決定する
        # 配置するコマンドの長さは、現在のx / y座標からプログラム端、またはコマンド配置済みの
        # セルに到達するまでのセル数となる
        # 進行方向のコマンド配置済みのセル数は、進行方向ではない方向の座標から求める
        if dp is DirectionPointer.RIGHT:
            offset_right: int = y
            length = w - offset_right - x
        elif dp is DirectionPointer.DOWN:
            offset_bottom: int = (w - 1) - x
            length = h - offset_bottom - y
        elif dp is DirectionPointer.LEFT:
            offset_left: int = (h - 1) - y
            length = x - offset_left + 1
        elif dp is DirectionPointer.UP:
            offset_top: int = x + 1
            length = y - offset_top + 1

        while True:
            if (abs(x - start_x) + abs(y - start_y)) == (length - 2):
                # 時計回り方向に回転するため、PUSH / POINTERコマンドを配置する
                push_color = get_color_from_command(Command.PUSH, color)
                pointer_color = get_color_from_command(Command.POINTER, push_color)

                if (self._is_conflict(push_color, grid, x, y) or
                    self._is_conflict(pointer_color, grid, x + dp.dx, y + dp.dy)):
                    # PUSH / POINTERコマンドの何れかが競合した

                    # PUSH / POINTERコマンドの配置箇所では競合解決が出来ないため、
                    # 2コマンド分戻した位置で競合の解決を行う
                    resolve_conflict(2)

                    # 競合の解決後はPUSH / POINTERコマンドの配置位置に戻されているため、
                    # 再度配置を行う
                    continue

                # PUSH / POINTERコマンドを配置
                # -> 1ライン分の配置完了

                for (command_, color_) in [(Command.PUSH, push_color),
                                           (Command.POINTER, pointer_color)]:
                    grid[y][x] = Codel(color_)

                    if self._trace:
                        print("put_codels_on_line: "
                              f"pos=({x}, {y}) command_index=--- "
                              f"command={command_} color={color_}")

                    if command_ is Command.POINTER:
                        dp = DirectionPointer.rotate(dp, 1)

                    color = color_
                    x += dp.dx
                    y += dp.dy

                break

            if command_index >= len(commands):
                # コマンド末尾まで配置したのでループを抜ける
                # -> 1ライン分の配置完了
                break

            # 配置するコマンドを取得し、そのコマンドの色を取得する
            command = commands[command_index]
            command_color = get_color_from_command(command, color)

            if self._is_conflict(command_color, grid, x, y):
                # 競合が発生

                # PUSH / POINTERコマンドの1セル手前で競合の解決を行うと、
                # POINTERコマンドが配置できなくなる
                # その場合は、1コマンド分戻した位置で競合の解決を行う
                resolve_conflict(1 if (abs(x - start_x) + abs(y - start_y)) == (length - 3) else 0)

                # 競合の解決後はPUSH / POINTERコマンドの配置位置である可能性があるため、
                # 競合が発生したコマンドを配置せず、ループ先頭の処理に戻す
                continue

            # コマンドの色から生成したCodelをgridに配置する
            grid[y][x] = Codel(command_color)

            if self._trace:
                print("put_codels_on_line: "
                      f"pos=({x}, {y}) command_index={command_index} "
                      f"command={command} color={command_color}")

            command_index += 1
            x += dp.dx
            y += dp.dy

            # 最後に配置したコマンドの色は、次に配置するコマンドの色の取得時に必要となるため、保存する
            color = command_color

        return command_index, x, y, dp, color

    def _put_to_empty_cells(self, grid: list[list[None | Codel]]) -> None:
        """
        空セルコマンド配置

        引数: grid で渡されたgrid中、Noneが設定されている、その時点で未使用の
        すべてのセルに対して、競合が発生しない任意の色を設定したCodelを配置する。

        Arguments:
            grid (list[list[None | Codel]]): 塗りつぶしを行うgrid
        """
        h: int = len(grid)
        w: int = len(grid[0])

        for y in range(h):
            for x in range(w):
                if grid[y][x]:
                    # 塗りつぶし対象外
                    continue

                exclude_colors: list[Color] = []

                while True:
                    random_color: Color = self._get_random_color(exclude_colors)

                    if self._is_conflict(random_color, grid, x, y):
                        exclude_colors.append(random_color)
                        # 競合発生 -> 色を変更してリトライ
                        continue

                    grid[y][x] = Codel(random_color)

                    if self._trace:
                        print(f"put_to_empty_cells: pos=({x}, {y}) command_index=--- "
                              f"command={LayoutCommand.NOT_USE} color={random_color}")

                    break

    def _dump_grid(self, grid: list[list[Codel | None]]) -> None:
        """
        dump

        引数: grid で渡されたgridの内容を標準出力に出力する。

        Arguments:
            grid (list[list[Codel | None]]): dumpするgrid
        """
        # dump用に (Command, Color) のtupleを生成
        w: int = len(grid[0])
        h: int = len(grid)
        dumps: list[list[None | tuple[Command | LayoutCommand, Color]]] = [
            [None] * w for _ in range(h)
        ]

        def _dump_abort_program_codels(
                grid: list[list[None | Codel]],
                dumps: list[list[None | tuple[Command | LayoutCommand, Color]]]) -> None:
            # 停止用プログラム部のdumpを生成
            initial_grid: list[list[None | Codel]] = self._create_grid(w, h, Color.WHITE)
            for y in range(h):
                for x in range(w):
                    initial_codel: Codel | None = initial_grid[y][x]
                    codel: Codel | None = grid[y][x]
                    if initial_codel and codel:
                        dumps[y][x] = (
                            LayoutCommand.ABORT if initial_codel.color is Color.WHITE else
                            Command.EDGE,
                            codel.color)

        def _dump_command_codels(
                grid: list[list[None | Codel]],
                dumps: list[list[None | tuple[Command | LayoutCommand, Color]]]) -> None:
            # プログラム開始位置から末尾までのdumpを生成
            if not grid[0][0]:
                # Codelが一つも配置されていない
                return

            x = 0
            y = 0
            dp = DirectionPointer.RIGHT
            before_color = grid[0][0].color
            abort_program_x = (len(grid[0]) - 1) // 2
            abort_program_y = len(grid) // 2

            while True:
                if (x == abort_program_x) and (y == abort_program_y):
                    # 停止用プログラムに到達
                    break

                codel: Codel | None = grid[y][x]
                if not codel:
                    # Codel未設定の箇所まで到達
                    break

                color = codel.color
                if color is None:
                    break

                command = get_command_from_color(before_color, color)
                dumps[y][x] = (command, color)

                if command is Command.POINTER:
                    dp = DirectionPointer.rotate(dp, 1)

                x += dp.dx
                y += dp.dy
                before_color = color

        def _dump_not_use_codels(
                grid: list[list[None | Codel]],
                dumps: list[list[None | tuple[Command | LayoutCommand, Color]]]) -> None:
            # プログラム未使用部のdumpを生成
            for y in range(h):
                for x in range(w):
                    codel: Codel | None = grid[y][x]
                    if (not dumps[y][x]) and codel:
                        dumps[y][x] = (LayoutCommand.NOT_USE, codel.color)

        # 内部関数を使用してdumpを生成
        _dump_abort_program_codels(grid, dumps)
        _dump_command_codels(grid, dumps)
        _dump_not_use_codels(grid, dumps)

        # 生成したdumpを1行ずつタブ文字区切りで出力
        print("\n".join(["\t".join(
              [f"({str(dump[0])} : {str(dump[1])})" if dump else "(empty)"
               for dump in row]) for row in dumps]))
