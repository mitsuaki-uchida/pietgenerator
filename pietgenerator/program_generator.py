"""
Pietプラグラム生成モジュール
"""
from io import BytesIO

from PIL import Image

from pietgenerator.command_generator.command_generator import ICommandGenerator
from pietgenerator.command_layouter.command_layouter import ICommandLayouter
from pietgenerator.piet_common import Codel, Color, Command


class GenerateProgramError(Exception):
    """
    GenerateProgramErrorは、Pietプログラムの生成に失敗した際に送出される例外である。
    """
    def __str__(self) -> str:
        """
        文字列表現

        Returns:
            str: 例外送出時のメッセージ
        """
        return f"{self.__class__.__name__}: generate Piet program failed."


class ProgramGenerator:
    """
    ProgramGeneratorは、Pietプラグラム生成器クラスである。
    インスタンス生成時に設定されたコマンド生成器 / コマンド配置器を使用して
    Pietプログラムの生成を行う。
    """

    def __init__(self,
                 command_generator: ICommandGenerator,
                 command_layouter: ICommandLayouter) -> None:
        """
        インスタンス初期化

        Arguments:
            command_generator (ICommandGenerator): コマンド生成器クラス
            command_layouter (ICommandLayouter): コマンド配置器クラス
        """
        super().__init__()
        self._command_generator = command_generator
        self._command_layouter = command_layouter

    def generate(self,
                 message: str,
                 start_color: Color = Color.LIGHT_RED,
                 abort_program_color: Color = Color.LIGHT_GREEN,
                 codel_size: int = 10) -> bytes:
        """
        Pietプラグラム生成

        引数: message を出力するPietプログラムを生成する。
        生成したPietプログラムは、PNG形式の画像ファイルのバイトオブジェクトとして返却する。

        Args:
            message (str): Pietプログラムが出力するメッセージ
            start_color (Color, optional): 原点に配置するCodelの色
            abort_program_color (Color, optional): 停止用プログラムに配置するCodelの色
            codel_size (int, optional): 1つのCodelのサイズ [px]

        Returns:
            bytes: Pietプログラムファイル(PNG形式の画像ファイル)

        Raises:
            GeneratorProgramError: Pietプログラムの生成に失敗した
        """
        try:
            commands: list[Command] = self._command_generator.generate(message)
            grid: list[list[Codel]] = self._command_layouter.do_layout(commands,
                                                                       start_color,
                                                                       abort_program_color)
            image: bytes = self._translate(grid, codel_size)

            return image
        except Exception as e:
            raise GenerateProgramError() from e

    def _translate(self, grid: list[list[Codel]], codel_size: int) -> bytes:
        """
        Pietプログラムファイル生成

        引数: grid で渡されたgridの色を基にPietプログラムファイルとなるPNG画像ファイルを生成する。

        Args:
            grid (list[list[Codel]]): PIL.Imageを生成するgrid
            codel_size (int): 1つのCodelのサイズ [px]

        Returns:
            bytes: Pietプログラムファイル(PNG形式の画像ファイル)
        """
        h = len(grid)
        w = len(grid[0])

        image = Image.new("RGBA", (w * codel_size, h * codel_size))

        for y in range(h):
            for x in range(w):
                r = grid[y][x].color.r
                g = grid[y][x].color.g
                b = grid[y][x].color.b
                a = grid[y][x].color.a

                for i in range(codel_size):
                    for j in range(codel_size):
                        image.putpixel(((x * codel_size) + j, (y * codel_size) + i), (r, g, b, a))

        fp: BytesIO = BytesIO()
        image.save(fp, format="PNG")

        return fp.getvalue()
