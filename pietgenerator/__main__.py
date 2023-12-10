"""
Pietプラグラム: mainモジュール
"""
import os
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

from pietgenerator.command_generator.factorize_generator import FactorizeCommandGenerator
from pietgenerator.command_layouter.square_layouter import SquareLayouter
from pietgenerator.piet_common import Color
from pietgenerator.program_generator import GenerateProgramError, ProgramGenerator


class Main:
    """
    Mainは、Pietプログラム生成モジュールのmainクラスである。
    """

    _PROG: str = "pietgenerator"
    """ 本プログラム名 """
    _USAGE: str = "usage: python -m pietgenerator [message] [output_path] [options]"
    """ 本プログラムのusage """

    @classmethod
    def main(cls) -> int:
        """
        mainメソッド

        本プログラムのエントリーポイントである。

        Returns:
            int: 終了ステータスコード
        """
        args: Any = None

        try:
            args = Main._create_argparser().parse_args()
        except SystemExit:
            # 終了ステータスコードをEX_USAGEにするため、SystemExitを捕捉
            # ArgumentParser.exit_on_error=Falseにした場合は、
            # 引数エラー時にArgumentErrorが送出されるが、その際に
            # ArgumentParser側でエラーメッセージを出力しないケースがあるため、
            # SystemExitを捕捉する
            return os.EX_USAGE

        message: str = args.message
        output_path: str = str(Path(args.output_path).absolute())
        start_color: Color = Color.name_of(args.start_color)
        end_color: Color = Color.name_of(args.end_color)
        codel_size: int = args.codel_size

        # codel_sizeが0以下の場合、画像の生成に失敗するため、別途判定
        if codel_size < 1:
            # 出力するエラーメッセージはArgumentParserの出力に寄せる
            print(cls._USAGE)
            print(f"{cls._PROG}: error: argument --codel_size: invalid int value: {codel_size}")
            return os.EX_USAGE

        image: bytes | None = None
        try:
            gen: ProgramGenerator = ProgramGenerator(FactorizeCommandGenerator(False),
                                                     SquareLayouter(False, False))
            image = gen.generate(message,
                                 start_color=start_color,
                                 abort_program_color=end_color,
                                 codel_size=codel_size)
        except GenerateProgramError:
            print(f"{cls._PROG}: error: internal error occurred.")
            return os.EX_SOFTWARE

        try:
            with open(output_path, "wb") as fp:
                fp.write(image)
        except OSError:
            print(f"{cls._PROG}: error: Piet program file create failed. path: '{output_path}'")
            return os.EX_OSERR

        print(f"{cls._PROG}: Piet program generate succeed. path: '{output_path}'")

        return os.EX_OK

    @classmethod
    def _create_argparser(cls) -> ArgumentParser:
        """
        ArgumentParser生成

        Returns:
            ArgumentParser: 生成したArgumentParser
        """
        choice_colors = [
            str(Color.LIGHT_RED), str(Color.RED), str(Color.DARK_RED),
            str(Color.LIGHT_YELLOW), str(Color.YELLOW), str(Color.DARK_YELLOW),
            str(Color.LIGHT_GREEN), str(Color.GREEN), str(Color.DARK_GREEN),
            str(Color.LIGHT_CYAN), str(Color.CYAN), str(Color.DARK_CYAN),
            str(Color.LIGHT_BLUE), str(Color.BLUE), str(Color.DARK_BLUE),
            str(Color.LIGHT_MAGENTA), str(Color.MAGENTA), str(Color.DARK_MAGENTA),
        ]

        arg_parser: ArgumentParser = ArgumentParser(
            prog=cls._PROG,
            usage=cls._USAGE,
            add_help=True,
            exit_on_error=True)

        arg_parser.add_argument(
            "message",
            help="Messages output by the program.",
            type=str)

        arg_parser.add_argument(
            "output_path",
            help="Output generated Piet program file path.",
            type=str)

        arg_parser.add_argument(
            "--start_color",
            help=("Start color of generated Piet program. "
                  "Default color is LIGHT_RED."),
            type=str,
            choices=choice_colors,
            default="LIGHT_RED")

        arg_parser.add_argument(
            "--end_color",
            help=("End color of generated Piet program. "
                  "Default color is LIGHT_GREEN."),
            type=str,
            choices=choice_colors,
            default="LIGHT_GREEN")

        arg_parser.add_argument(
            "--codel_size",
            help=("Pixel size of Codel. "
                  "Set an int value greater than 0. "
                  "Default size is 10 pixels."),
            type=int,
            default=10)

        return arg_parser


if __name__ == '__main__':
    # mainメソッドを実行し、終了ステータスコードで終了する
    sys.exit(Main.main())
