"""
Pietプラグラム: メッセージ出力コマンド生成器モジュール（素因数分解アルゴリズム）
"""
from typing import Any

from pietgenerator.command_generator.command_generator import ICommandGenerator
from pietgenerator.piet_common import Command


class FactorizeCommandGenerator(ICommandGenerator):
    """
    FactorizeCommandGeneratorは、Pietプラグラムのメッセージ出力コマンド生成器クラスである。
    メッセージからコマンドを生成する際、メッセージの文字を表すASCIIコードを小さい数に分解する
    アルゴリズムとして、素因数分解を使用する。
    ※ 厳密には FactorizeCommandGenerator._DEVS で指定した数値、および -1 に分解する。
    """

    _DEVS = [2, 3]
    """
    メッセージの文字を表すASCIIコードを素因数分解する際に使用する除数
    ASCIIコードは _DEVS 内の数値、および -1 を含むリストに分解される。
    """

    def __init__(self, debug: bool = True) -> None:
        """
        インスタンス初期化

        Arguments:
            debug (bool): True: デバッグログ有効化; False: デバッグログ無効化
        """
        super().__init__(debug)

    def _generate_impl(self, message: str) -> list[Command]:
        """
        メッセージ -> コマンド生成実装

        ICommandGenerator.generateメソッドの実装を行う。

        Arguments:
            message (str): コマンドを生成するメッセージ

        Returns:
            list[Command]: メッセージから生成されたコマンドのリスト

        Raises:
            GenerateCommandError: コマンドの生成に失敗した
        """
        # 先頭にNONEコマンドを格納
        commands: list[Command] = [Command.NONE]

        # メッセージを後方から一文字ずつコマンドに変換して格納
        for ch in message[::-1]:
            commands.extend(self._character_to_commands(ch))

        # メッセージの文字数分、OUT_CHARコマンドを格納
        commands.extend([Command.OUT_CHAR] * len(message))

        if self._debug:
            print(f"generate_impl: exit. commands={[str(command) for command in commands]}")

        return commands

    def _character_to_commands(self, character: str) -> list[Command]:
        """
        文字 -> コマンド変換

        引数: character をコマンドに変換する。

        Arguments:
            character (str): コマンドに変換する文字

        Returns:
            list[Command]: 文字から生成されたコマンドのリスト
        """
        factorized: list[int | list[Any]] = self._factorize(ord(character), self._DEVS)
        commands: list[Command] = self._values_to_commands(factorized)

        if self._debug:
            print("character_to_commands: "
                  f"character='{character}'({ord(character):02x}) "
                  f"factorized={factorized} "
                  f"commands={[str(command) for command in commands]}")

        return commands

    def _factorize(self, value: int, devs: list[int]) -> list[int | list[Any]]:
        """
        素因数分解

        引数: value を 引数: devs に格納されている値、および -1 に素因数分解する。
        値が引数: devs で割り切れない場合は、1 を加算した上で、再帰的に素因数分解を行い、
        末尾に -1 を格納する。
        ただし、引数: value が 1 である場合のみ、例外として 1 を格納する。

        Arguments:
            value (int): 素因数分解する0より大きい整数
            devs (list[int]): 使用する素因数のリスト

        Returns:
            list[int | list[Any]]: value を素因数分解した値のリスト

        Raises:
            ValueError: 引数: value が1未満の値である

        Note:
            仕様通りに動作するには、引数: devs には素数が格納されている必要があるが、
            現状では引数: devs には固定値 (_DEVS) のみ設定されるため、正当性のチェックは行わない。

        Examples:
            >>> MessageOutputCommandGenerator gen = MessageOutputCommandGenerator()
            >>> print(gen._factorize(1, [2, 3]))
            [1]                     # 1 = 1
            >>> print(gen._factorize(2, [2, 3]))
            [2]                     # 2 = 2
            >>> print(gen._factorize(3, [2, 3]))
            [3]                     # 3 = 3
            >>> print(gen._factorize(4, [2, 3]))
            [2, 2]                  # 4 = 2 x 2
            >>> print(gen._factorize(5, [2, 3]))
            [2, 3, -1]              # 5 = 2 x 3 - 1
            >>> print(gen._factorize(10, [2, 3]))
            [2, [2, 3, -1]]         # 10 = 2 x (2 x 3 - 1)
            >>> print(gen._factorize(21, [2, 3]))
            [2, [2, 2, 3, -1], -1]  # 21 = 2 x (2 x 2 x 3 - 1) - 1
        """
        if value < 1:
            # 1未満の値は計算不可
            raise ValueError(f"value: '{value}' is less than 1.")

        values: list[Any] = []

        if value == 1:
            values.append(value)
            return values

        while value > 1:
            for dev in devs:
                if (value % dev) == 0:
                    values.append(dev)
                    value = value // dev
                    break
            else:
                # devs内の値で割り切れない場合は、+ 1 して再入し、末尾に -1 を格納
                factorized_values = self._factorize(value + 1, devs)
                factorized_values.append(-1)

                # valuesが空である場合は、listが二重にならないよう、appendではなく代入する
                if not values:
                    values = factorized_values
                else:
                    values.append(factorized_values)

                break

        return values

    def _values_to_commands(self,
                            values: list[int | list[Any]],
                            before_value: int = 0) -> list[Command]:
        """
        素因数分解した値リスト -> コマンド変換

        引数: values をPietインタプリタが実行するコマンドに変換する。
        Pietインタプリタの記憶領域はstackであるため、逆ポーランド記法となるようにコマンドを格納する。
        コマンド数を削減するため、直前にstackに格納した値は出来るだけ再利用する。

        Arguments:
            values (list[int | list[Any]]): factorizeメソッドで素因数分解した値のリスト
            before_value (int): 直前にstackに格納した値

        Returns:
            list[Command]: 実行時に values の計算結果となるコマンドのリスト

        Todo:
            values に大きな値が格納されている場合、現状のアルゴリズムでは非効率であるため、要再検討。

        Examples:
            >>> MessageOutputCommandGenerator gen = MessageOutputCommandGenerator()
            >>> print([str(command) for command in gen._values_to_commands([1])]
            [PUSH]
            >>> print([str(command) for command in gen._values_to_commands([2])]
            [PUSH, PUSH, ADD]
            >>> print([str(command) for command in gen._values_to_commands([3])]
            [PUSH, PUSH, ADD, PUSH, ADD]
            >>> print([str(command) for command in gen._values_to_commands([2, 2])]
            [PUSH, PUSH, ADD, DUPLICATE, MULTIPLY]
            >>> print([str(command) for command in gen._values_to_commands([2, 3, -1])]
            [PUSH, PUSH, ADD, DUPLICATE, PUSH, ADD, MULTIPLY, PUSH, SUBTRACT]
            >>> print([str(command) for command in gen._values_to_commands([2, [2, 3, -1]])]
            [PUSH, PUSH, ADD, DUPLICATE, DUPLICATE, PUSH, ADD, MULTIPLY, PUSH, SUBTRACT, MULTIPLY]
        """
        commands: list[Command] = []

        for value in values:
            if isinstance(value, list):
                # リストがネストしている場合は再入
                commands.extend(self._values_to_commands(value, before_value))
                # 直前の値を使用すると不利益が大きいためクリア
                before_value = 0
            elif isinstance(value, int):
                if value == -1:
                    # ここでは -1 は処理しない
                    continue

                if before_value == 0:
                    # 直前の値が 0:
                    # その値になるまで、PUSHコマンド / ADDコマンドを繰り返し実行
                    commands.append(Command.PUSH)
                    commands.extend([Command.PUSH, Command.ADD] * (value - 1))
                elif before_value == value:
                    # 直前の値と一致:
                    # stack先頭の値を複製するため、DUPLICATEコマンドを実行
                    commands.append(Command.DUPLICATE)
                elif before_value < value:
                    # 直前の値より大:
                    # stack先頭の値を複製するため、DUPLICATEコマンドを実行
                    # 複製した値との差になるまで、PUSHコマンド / ADDコマンドを繰り返し実行
                    commands.append(Command.DUPLICATE)
                    commands.extend([Command.PUSH, Command.ADD] * (value - before_value))
                elif before_value > value:
                    # 直前の値より小:
                    # stack先頭の値を複製するため、DUPLICATEコマンドを実行
                    # 複製した値との差になるまで、PUSHコマンド / SUBTRACTコマンドを繰り返し実行
                    commands.append(Command.DUPLICATE)
                    commands.extend([Command.PUSH, Command.SUBTRACT] * (before_value - value))

                before_value = value

        if values[-1] != -1:
            # すべての値で乗算を行うため、(値の数 - 1) 分、MULTIPLYコマンドを格納
            commands.extend([Command.MULTIPLY] * (len(values) - 1))
        else:
            # -1 以外のすべての値で乗算を行うため、(値の数 - 2) 分、MULTIPLYコマンドを格納
            commands.extend([Command.MULTIPLY] * (len(values) - 2))
            # PUSHコマンド / SUBTRACTコマンドを格納
            commands.extend([Command.PUSH, Command.SUBTRACT])

        return commands
