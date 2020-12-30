#!/usr/bin/env python3
# based on the version v1 by HenryEx
import os

script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)


class Item:
    def __init__(self, **lang):
        self.lang = lang

    def __get__(self, obj: 'I18n', objtype=None) -> str:
        return self.lang.get(obj.lang, self.lang['en'])


class I18n:
    lang: str = None
    welcome = Item(
        en="Based on the MHP2G save tools v1 made by HenryEx - rewritten in python by fduxiao",
        zh='基于HenryEx的MHP2G存档修改工具v1 - python重写版, Github@fduxiao',
    )
    choose_game = Item(
        en="There are three versions of this game. Please choose the one of your save: ",
        zh="MHP2G有欧版、美版、日版(中文)，请选择你存档的版本：",
    )
    input_number = Item(
        en="Please input an number: ",
        zh="请输入号码：",
    )
    nonexistent_number = Item(
        en="Please choose an existent number! ",
        zh="请选择存在的号码！",
    )
    choose_action = Item(
        en="Choose what you want to do. ",
        zh="请选择你要进行的操作",
    )
    actions = Item(
        en="[1] PSP Save Decryption \t"
           "[2] PSP Save Encryption \n"
           "[3] Game Save Decryption\t"
           "[4] Game Save Encryption\n"
           "\n"
           "[5] Quest Downloader\n"
           "[6] Quest Packer / Unpacker\n"
           "\n"
           "[0] Exit\n",
        zh="[1] PSP存档解密 \t"
           "[2] PSP存档加密 \n"
           "[3] 游戏存档解密\t"
           "[4] 游戏存档加密\n"
           "\n"
           "[5] 任务下载\n"
           "[6] 任务打包/解包\n"
           "\n"
           "[0] Exit\n",
    )
    action_not_implemented = Item(
        en="This action has not been implemented yet :(",
        zh="操作尚未实现. "
    )

    decrypted = Item(
        en="Your save seems decrypted. ",
        zh="你的存档看上去已解密"
    )

    fail_to_decrypt = Item(
        en="Fail to decrypt. ",
        zh="解密失败"
    )

    encrypted = Item(
        en="Your save seems encrypted. ",
        zh="你的存档看上去已加密"
    )

    fail_to_encrypt = Item(
        en="Fail to encrypt. ",
        zh="加密失败"
    )

    psp_decrypt = Item(
        en="PSP encrypts save files with a hardware chip. This process is reverse engineered and thus not reliable. "
        "Please make sure to backup your save. I am not responsible for your loss.\n"
        "Do you still want to try it? \n\n"
        "[1] Decrypt\n"
        "[0] Return to main menu\n",
        zh="PSP用了特殊芯片加密存档，这一过程是逆向结果，并不可靠。 请备份数据并自负损失。\n"
        "是否还要继续？\n\n"
        "[1] 解密\n"
        "[0] 返回主菜单\n",
    )


def check_encrypted(size) -> bool:
    if size == 1483024:
        return True
    if size == 1483008:
        return False
    raise NotImplementedError(f"Unknown size: {size}")


def decrypt():
    pass


def encrypt():
    pass


class SaveTools:
    game = None
    key = None

    def __init__(self):
        self.i18n = I18n()
        self.flashes = []

    @property
    def save_size(self) -> int:
        return os.stat('MHP2NDG.bin').st_size

    @property
    def encrypted(self) -> bool:
        return check_encrypted(self.save_size)

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        if self.flashes:
            for i in self.flashes:
                print(i)
            self.flashes = []
            print()
            print()

    def flash(self, msg):
        self.flashes.append(msg)

    def lang(self):
        self.clear()
        print('Please select your language. 请选择你的语言')
        print('[1] English')
        print('[2] 中文')
        print()
        x = input('Please input the number. 请输入号码: ')
        x = {
            '1': 'en',
            '2': 'zh',
        }.get(x, None)
        if x is None:
            self.flash('Please choose an existent number! 请选择存在的号码！')
            # tail recursion
            return self.lang()
        self.i18n.lang = x

    def welcome(self):
        self.clear()
        print(self.i18n.welcome)
        print()
        print(self.i18n.choose_game)
        print('[1] Monster Hunter Freedom Unite EU(欧) (ULES01213)')
        print('[2] Monster Hunter Freedom Unite US(美) (ULUS10391)')
        print('[3] Monster Hunter Portable 2nd G(中日) (ULJM05500)')
        print()
        x = input(self.i18n.input_number)
        if x == '1':
            self.game = 'MHP2G_EU'
            self.key = 'MHFU_key.bin'
        elif x == '2':
            self.game = 'MHP2G_EU'
            self.key = 'MHFU_key.bin'
        elif x == '3':
            self.game = 'MHP2G_JP'
            self.key = 'MHP2g_key.bin'
        else:
            self.flash(self.i18n.nonexistent_number)
            return self.welcome()

    def psp_decrypt(self):
        self.clear()
        print(self.i18n.psp_decrypt)
        x = input(self.i18n.input_number)
        if x == '1':
            if not self.encrypted:
                self.flash(self.i18n.decrypted)
                return self.main()
            # decrypt
            decrypt()
            if self.encrypted:
                self.flash(self.i18n.fail_to_decrypt)
                return self.psp_decrypt()
            self.flash(self.i18n.decrypted)
            return self.main()
        elif x == '0':
            return self.main()
        else:
            self.flash(self.i18n.nonexistent_number)
            return self.psp_decrypt()

    def psp_encrypt(self):
        self.flash("psp encrypt")
        self.main()

    def game_decrypt(self):
        self.flash("game decrypt")
        self.main()

    def game_encrypt(self):
        self.flash("game encrypt")
        self.main()

    def pack_unpack(self):
        self.flash("pack unpack")
        self.main()

    def main(self):
        if self.i18n.lang is None:
            self.lang()

        if self.game is None:
            self.welcome()

        self.clear()
        print(self.i18n.choose_action)
        print(self.i18n.actions)

        x = input(self.i18n.input_number)
        if x == '1':
            return self.psp_decrypt()
        elif x == '2':
            return self.psp_encrypt()
        elif x == '3':
            return self.game_decrypt()
        elif x == '4':
            return self.game_encrypt()
        elif x == '5':
            self.flash(self.i18n.action_not_implemented)
            return self.main()
        elif x == '6':
            self.pack_unpack()
        elif x == '0':
            return
        else:
            self.flash(self.i18n.nonexistent_number)
            return self.main()


if __name__ == '__main__':
    SaveTools().main()
