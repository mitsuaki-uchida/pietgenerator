"""
Piet言語共通モジュール
"""
from enum import Enum
from typing import Self


class DirectionPointer(Enum):
    """
    DirectionPointerは、Piet言語のDirection Pointer(DP)を実現するクラスである。
    """

    RIGHT = (0, 1, 0)
    """ 右 """
    DOWN = (1, 0, 1)
    """ 下 """
    LEFT = (2, -1, 0)
    """ 左 """
    UP = (3, 0, -1)
    """ 上 """

    def __init__(self, index: int, dx: int, dy: int) -> None:
        """
        インスタンス初期化

        Arguments:
            index (int): index(0 - 3)
            dx (int): x軸方向の移動量
            dy (int): y軸方向の移動量
        """
        self._index = index
        self._dx = dx
        self._dy = dy

    def __str__(self) -> str:
        """
        文字列表現

        Returns:
            str: 自身の名前
        """
        return self.name

    @property
    def index(self) -> int:
        """
        index取得

        Returns:
            int: index(0 - 3)
        """
        return self._index

    @property
    def dx(self) -> int:
        """
        x軸方向の移動量取得

        Returns:
            int: x軸方向の移動量
        """
        return self._dx

    @property
    def dy(self) -> int:
        """
        y軸方向の移動量取得

        Returns:
            int: y軸方向の移動量
        """
        return self._dy

    @classmethod
    def rotate(cls, dp: Self, num: int) -> Self:
        """
        DirectionPointer回転

        引数: dp で渡されたDirectionPointerを、時計回り方向に引数: num 回分 1 / 4 回転する。
        引数: num が負の値である場合は、反時計回りに回転する。

        Arguments:
            dp (DirectionPointer): 回転前のDirectionPointer
            num (int): 時計回りに 1 / 4 回転する回数
                        負の値である場合は反時計回りに 1 / 4 回転する回数

        Returns:
            DirectionPointer: 回転後のDirectionPointer
        """
        return cls.index_of((dp.index + num) % len(cls))

    @classmethod
    def index_of(cls, index: int) -> Self:
        """
        index -> DirectionPointer取得

        indexが一致するDirectionPointerを取得する。

        Arguments:
            index (int): index(0 - 3)

        Returns:
            DirectionPointer: indexが一致するDirectionPointer

        Raises:
            ValueError: indexが一致するDirectionPointerが存在しない
        """
        for dp in cls:
            if dp.index == index:
                return dp

        raise ValueError(f"{index} is not found.")


class CodelChooser(Enum):
    """
    CodelChooserは、Piet言語のCodelChooser(CC)を実現するクラスである。
    """

    RIGHT = 0
    """ 右 """
    LEFT = 1
    """ 左 """

    def __init__(self, value) -> None:
        """
        インスタンス初期化

        Arguments:
            index (int): index(0 - 1)
        """
        self._index = value

    def __str__(self) -> str:
        """
        文字列表現

        Returns:
            str: 自身の名前
        """
        return self.name

    @property
    def index(self) -> int:
        """
        index取得

        Returns:
            int: index
        """
        return self._index

    @classmethod
    def switch(cls, cc: Self, num: int) -> Self:
        """
        CodelChooser切り替え

        引数: cc で渡されたCodelChooserの左右を引数: num 回分切り替える。

        Arguments:
            cc (CodelChooser): 現在の (切り替え前の) CodelChooser
            num (int): 左右切り替えを行う回数

        Returns:
            CodelChooser: 切り替え後のCodelChooser
        """
        return cls.index_of((cc.index + num) % len(cls))

    @classmethod
    def index_of(cls, index: int) -> Self:
        """
        index -> CodelChooser取得

        indexが一致するCodelChooserを取得する。

        Arguments:
            index (int): index(0 - 1)

        Returns:
            CodelChooser: indexが一致するCodelChooser

        Raises:
            ValueError: indexが一致するCodelChooserが存在しない
        """
        for cc in cls:
            if cc.index == index:
                return cc

        raise ValueError(f"{index} is not found.")


class Command(Enum):
    """
    Commandは、Piet言語のCommandを実現するクラスである。
    """

    NONE = (0, 0, 0)
    """ NONEコマンド """
    PUSH = (1, 0, 1)
    """ PUSHコマンド """
    POP = (2, 0, 2)
    """ POPコマンド """
    ADD = (3, 1, 0)
    """ ADDコマンド """
    SUBTRACT = (4, 1, 1)
    """ SUBTRACTコマンド """
    MULTIPLY = (5, 1, 2)
    """ MULTIPLYコマンド """
    DIVIDE = (6, 2, 0)
    """ DIVIDEコマンド """
    MOD = (7, 2, 1)
    """ MODコマンド """
    NOT = (8, 2, 2)
    """ NOTコマンド """
    GREATER = (9, 3, 0)
    """ GREATERコマンド """
    POINTER = (10, 3, 1)
    """ POINTERコマンド """
    SWITCH = (11, 3, 2)
    """ SWITCHコマンド """
    DUPLICATE = (12, 4, 0)
    """ DUPLICATEコマンド """
    ROLL = (13, 4, 1)
    """ ROLLコマンド """
    IN_NUMBER = (14, 4, 2)
    """ IN_NUMBERコマンド """
    IN_CHAR = (15, 5, 0)
    """ IN_CHARコマンド """
    OUT_NUMBER = (16, 5, 1)
    """ OUT_NUMBERコマンド """
    OUT_CHAR = (17, 5, 2)
    """ OUT_CHARコマンド """
    FREE_ZONE = (100, 0, 0)
    """ FREE_ZONEコマンド (白色Codel用) """
    EDGE = (101, 0, 0)
    """ EDGEコマンド (黒色Codel用)  """

    def __init__(self, command_id: int, hue_step: int, lightness_step: int) -> None:
        """
        インスタンス初期化

        Arguments:
            command_id (int): コマンドを示す一意のID
            hue_step (int): 色相の変化量(0 - 5)
            lightness_step (int): 明度の変化量(0 - 2)
        """
        self._command_id = command_id
        self._hue_step = hue_step
        self._lightness_step = lightness_step

    def __str__(self) -> str:
        """
        文字列表現

        Returns:
            str: 自身の名前
        """
        return self.name

    @property
    def hue_step(self) -> int:
        """
        色相の変化量取得

        Returns:
            int: 色相の変化量(0 - 5)
        """
        return self._hue_step

    @property
    def lightness_step(self) -> int:
        """
        明度の変化量取得

        Returns:
            int: 明度の変化量(0 - 2)
        """
        return self._lightness_step

    @classmethod
    def get_command(cls, hue_step: int, lightness_step: int) -> Self:
        """
        色相差 / 明度差 -> Command取得

        色相差 / 明度差が一致するCommandを取得する。

        Arguments:
            hue_step (int): 色相差(0 - 5)
            lightness_step (int): 明度差(0 - 2)

        Returns:
            Command: 色相差 / 明度差が一致するCommand

        Raises:
            ValueError: 色相差 / 明度差が一致するCommandが存在しない
        """
        for command in cls:
            if (command.hue_step == hue_step) and (command.lightness_step == lightness_step):
                return command

        raise ValueError(f"command=({hue_step}, {lightness_step}) is not found.")


class Color(Enum):
    """
    Colorは、Piet言語のColorを実現するクラスである。
    """

    BLACK = (0x000000, None, None)
    """ BLACK (0x000000) (色相 / 明度なし) """
    WHITE = (0xFFFFFF, None, None)
    """ WHITE (0xFFFFFF) (色相 / 明度なし) """

    LIGHT_RED = (0xFFC0C0, 0, 0)
    """ LIGHT RED (0xFFC0C0) """
    LIGHT_YELLOW = (0xFFFFC0, 1, 0)
    """ LIGHT YELLOW (0xFFFFC0) """
    LIGHT_GREEN = (0xC0FFC0, 2, 0)
    """ LIGHT GREEN (0xC0FFC0) """
    LIGHT_CYAN = (0xC0FFFF, 3, 0)
    """ LIGHT CYAN (0xC0FFFF) """
    LIGHT_BLUE = (0xC0C0FF, 4, 0)
    """ LIGHT BLUE (0xC0C0FF) """
    LIGHT_MAGENTA = (0xFFC0FF, 5, 0)
    """ LIGHT MAGENTA (0xFFC0FF) """
    RED = (0xFF0000, 0, 1)
    """ RED (0xFF0000) """
    YELLOW = (0xFFFF00, 1, 1)
    """ YELLOW (0xFFFF00) """
    GREEN = (0x00FF00, 2, 1)
    """ GREEN (0x00FF00) """
    CYAN = (0x00FFFF, 3, 1)
    """ CYAN (0x00FFFF) """
    BLUE = (0x0000FF, 4, 1)
    """ BLUE (0x0000FF) """
    MAGENTA = (0xFF00FF, 5, 1)
    """ MAGENTA (0xFF00FF) """
    DARK_RED = (0xC00000, 0, 2)
    """ DARK RED (0xC00000) """
    DARK_YELLOW = (0xC0C000, 1, 2)
    """ DARK YELLOW (0xC0C000) """
    DARK_GREEN = (0x00C000, 2, 2)
    """ DARK GREEN (0x00C000) """
    DARK_CYAN = (0x00C0C0, 3, 2)
    """ DARK CYAN (0x00C0C0) """
    DARK_BLUE = (0x0000C0, 4, 2)
    """ DARK BLUE (0x0000C0) """
    DARK_MAGENTA = (0xC000C0, 5, 2)
    """ DARK MAGENTA (0xC000C0) """

    COLOR_MAX = (None, 6, 3)
    """ 色相 / 明度最大値 """

    def __init__(self, rgb: int, hue: int, lightness: int) -> None:
        """
        インスタンス初期化

        Arguments:
            rgb (int): 0xRRGGBBで表現する24bitカラーコード
            hue (int): 色相(0 - 5)
            lightness (int): 明度(0 - 2)
        """
        self._rgb = rgb
        self._hue = hue
        self._lightness = lightness

    def __str__(self) -> str:
        """
        文字列表現

        Returns:
            str: 自身の名前
        """
        return self.name

    @property
    def hue(self) -> int:
        """
        色相取得

        Returns:
            int: 色相(0 - 5)
        """
        return self._hue

    @property
    def lightness(self) -> int:
        """
        明度取得

        Returns:
            int: 明度(0 - 2)
        """
        return self._lightness

    @property
    def r(self) -> int:
        """
        カラーコード(赤)取得

        Returns:
            int: カラーコード(赤: 0x00 - 0xFF)
        """
        return (self._rgb >> 16) & 0xff

    @property
    def g(self) -> int:
        """
        カラーコード(緑)取得

        Returns:
            int: カラーコード(緑: 0x00 - 0xFF)
        """
        return (self._rgb >> 8) & 0xff

    @property
    def b(self) -> int:
        """
        カラーコード(青)取得

        Returns:
            int: カラーコード(青: 0x00 - 0xFF)
        """
        return self._rgb & 0xff

    @property
    def a(self) -> int:
        """
        カラーコード(アルファ)取得

        本プロパティは常に不透過(0xFF)を返却する。

        Returns:
            int: カラーコード(アルファ: 0xFF)
        """
        return 0xff

    @classmethod
    def get_color(cls, hue: int, lightness: int) -> Self:
        """
        色相 / 明度 -> Color取得

        色相 / 明度が一致するColorを取得する。

        Arguments:
            hue (int): 色相(0 - 5)
            lightness (int): 明度(0 - 2)

        Returns:
            Color: 色相 / 明度が一致するColor

        Raises:
            ValueError: 色相 / 明度が一致するColorが存在しない
        """
        if (hue >= cls.COLOR_MAX.hue) or (lightness >= cls.COLOR_MAX.lightness):
            raise ValueError(f"color=({hue}, {lightness}) is out of range.")

        for color in cls:
            if (color.hue == hue) and (color.lightness == lightness):
                return color

        raise ValueError(f"color=({hue}, {lightness}) is not found.")

    @classmethod
    def name_of(cls, name: str) -> Self:
        """
        名前 -> Color取得

        名前が一致するColorを取得する。

        Arguments:
            name (str): 名前

        Returns:
            Color: 名前が一致するColor

        Raises:
            ValueError: 名前が一致するColorが存在しない
        """
        for color in cls:
            if color.name == name:
                return color

        raise ValueError(f"name={name} is not found.")


class Codel:
    """
    Codelは、Piet言語のCodelを実現するクラスである。
    """

    def __init__(self, color: Color) -> None:
        """
        インスタンス初期化

        Arguments:
            color (Color): Codelに設定するColor
        """
        self._color = color

    def __str__(self) -> str:
        """
        文字列表現

        Returns:
            str: 自身を表す文字列
        """
        return f"({str(self._color)})"

    @property
    def color(self) -> Color:
        """
        色取得

        Returns:
            Color: 自身に設定されている色
        """
        return self._color


def get_color_from_command(command: Command, color: Color) -> Color:
    """
    実行コマンド色取得

    引数: color のCodelから引数: command を実行する場合に、そのコマンドとなる
    色相差 / 明度差の色を取得する。

    Arguments:
        command (Command): 実行するコマンド
        color (Color): コマンドを実行する直前の色

    Returns:
        Color: 実行するコマンドの色
    """
    # commandの色相 / 明度を算出
    hue = (color.hue + command.hue_step) % Color.COLOR_MAX.hue
    lightness = (color.lightness + command.lightness_step) % Color.COLOR_MAX.lightness

    # 色相 / 明度が一致するColorを取得
    return Color.get_color(hue, lightness)


def get_command_from_color(color: Color, next_color: Color) -> Command:
    """
    色により実行されるコマンド取得

    引数: color のCodelから引数: next_color のCodelに移動した際の色相差 / 明度差から
    実行するコマンドを取得する。

    Arguments:
        color (Color): コマンドを実行する直前の色
        next_color (Color): 実行するコマンドの色

    Returns:
        Color: 実行するコマンド
    """
    if color is Color.WHITE:
        return Command.NONE

    if next_color is Color.WHITE:
        return Command.FREE_ZONE

    # commandの色相 / 明度を算出
    hue_step = ((Color.COLOR_MAX.hue + next_color.hue - color.hue)
                % Color.COLOR_MAX.hue)
    lightness_step = ((Color.COLOR_MAX.lightness + next_color.lightness - color.lightness)
                      % Color.COLOR_MAX.lightness)

    # 色相差 / 明度差が一致するCommandを取得
    return Command.get_command(hue_step, lightness_step)
