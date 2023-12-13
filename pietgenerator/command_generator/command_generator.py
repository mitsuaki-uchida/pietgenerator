"""
Pietプラグラム: メッセージ出力コマンド生成器インタフェースモジュール
"""
import abc
from typing import NoReturn

from pietgenerator.piet_common import Command


class GenerateCommandError(Exception):
    """
    GenerateCommandErrorは、コマンドの生成に失敗した際に送出される例外である。
    """
    def __str__(self) -> str:
        """
        文字列表現

        Returns:
            str: 例外送出時のメッセージ
        """
        return f"{self.__class__.__name__}: generate command failed."


class ICommandGenerator(metaclass=abc.ABCMeta):
    """
    ICommandGeneratorは、Pietプラグラムのメッセージ出力コマンド生成器のインタフェースクラスである。
    メッセージ出力コマンド生成器クラスは本クラスを継承し、未実装のインタフェースを定義すること。
    """

    def __init__(self, debug: bool) -> None:
        """
        インスタンス初期化

        Arguments:
            debug (bool): True: デバッグログ有効化; False: デバッグログ無効化
        """
        super().__init__()
        self._debug = debug

    def generate(self, message: str) -> list[Command]:
        """
        メッセージ -> コマンド生成

        引数: message からそのメッセージを出力するコマンドのリストを生成する。
        本メソッドは以下の責務を持つ。

        - コマンドのリストの先頭にNONEコマンドを格納すること。
        - メッセージ文字数分のOUT_CHARコマンドを格納すること。
        - コマンドをリストの先頭から実行した際に、メッセージが正しく出力されること。

        Arguments:
            message (str): コマンドを生成するメッセージ

        Returns:
            list[Command]: メッセージから生成されたコマンドのリスト

        Raises:
            GenerateCommandError: コマンドの生成に失敗した
        """
        try:
            return self._generate_impl(message)
        except Exception as e:
            raise GenerateCommandError() from e

    @abc.abstractmethod
    def _generate_impl(self, message: str) -> list[Command] | NoReturn:
        """
        メッセージ -> コマンド生成実装

        ICommandGenerator.generateメソッドの実装を行う。
        本メソッドはインタフェースの宣言であるため、常にNotImplementedErrorを送出する。

        Arguments:
            message (str): コマンドを生成するメッセージ

        Raises:
            NotImplementedError: 本メソッドを呼び出した場合
        """
        raise NotImplementedError
