from pathlib import Path
import argparse
import shutil
from recurser import Recurser
import pyexiv2
import pyperclip
from rich import print


class Base(Recurser):
    def __init__(self, path, src_dpath, extname, movedirname, recursive=True, resolve=True,):
        self.movedirname = movedirname
        self.extname = extname
        # check RAW and JPG dir
        self.src_dpath = Path(src_dpath).resolve().expanduser()
        if not self.src_dpath.exists() or not Path(path).exists():
            raise FileNotFoundError('Not found JPG or RAW dir. please check...')
        # destination dir
        self.dst_dpath = self.src_dpath.parent / Path(self.movedirname)
        if not self.dst_dpath.exists():
            self.dst_dpath.mkdir()
        super().__init__(path, recursive, resolve)

    def rename(self, path):
        raw_name = path.with_suffix(self.extname).name
        src_fpath = self.src_dpath / raw_name
        dst_fpath = self.dst_dpath / raw_name
         # check exists
        if not src_fpath.exists():
            print(f"[yellow]not hit...[/] - [red]{src_fpath.name}[/]")
            return {'nothit':str(path)}
        # check exists and overwrite
        if dst_fpath.exists():
            print(f"[yellow]file exists. dont't move.[/] - [red]{src_fpath.name}[/]")
            return {'exists':str(path)}
        print(f"[green]hit![/] - {src_fpath.name}")
        shutil.move(src_fpath, dst_fpath)


class Adoberating(Base):
    def func(self, path) -> list:
        with pyexiv2.Image(str(path)) as img:
            xmp = img.read_xmp()
        adobe_star = xmp.get('Xmp.xmp.Rating')
        if adobe_star == None:
            adobe_star = '0'
        if int(adobe_star) > 0:
            # mv hit filename
            self.rename(path)
        else:
            pass


class Pasteboard(Base):
    def __init__(self, path, src_dpath, extname, movedirname, recursive=True, resolve=True):
        super().__init__(path, src_dpath, extname, movedirname, recursive, resolve)
        # paste board date into 'self.items'
        p = pyperclip.paste().split()
        self.items = (Path(i) for i in p)

    def func(self, path):
        self.rename(path)


class File(Base):
    def func(self, path):
        self.rename(path)


def __cli_adobe_rating(args):
    print("[magenta]adobe raiting mode[/]")
    matti = Adoberating(path=args.input, src_dpath=args.srcpath, extname=args.raw_extension, movedirname=args.moved_dir)
    matti.get_files('.jpg')
    matti.multi_exec()


def __cli_paste_board(args):
    print("[magenta]paste board mode[/]")
    matti = Pasteboard(path='.', src_dpath=args.srcpath, extname=args.raw_extension, movedirname=args.moved_dir)
    matti.multi_exec()
    pass


def __cli_file(args):
    print("[magenta]file mode[/]")
    matti = File(path=args.input, src_dpath=args.srcpath, extname=args.raw_extension, movedirname=args.moved_dir)
    matti.get_files('.jpg')
    matti.multi_exec()
          

def cli():
    parser = argparse.ArgumentParser(description='select file finder from Adobe raiting.')  
    subparsers = parser.add_subparsers()
    parser.add_argument('--raw-extension', default='.CR2', help='setting: raw date extention.')
    parser.add_argument('--moved-dir', default='SELECT', help='setting: move dir name.')

    parser_ra = subparsers.add_parser('ra', help="matti raiting mode")
    parser_ra.add_argument('srcpath', nargs='?', default='.', help="check raw directry.")
    parser_ra.add_argument('-i', '--input', nargs='?', help='search jpg directry.')
    parser_ra.set_defaults(handler=__cli_adobe_rating)

    parser_pb = subparsers.add_parser('pb', help="matti pasteboard mode")
    parser_pb.add_argument('srcpath', nargs='?', default='.', help="check raw directry.")
    parser_pb.set_defaults(handler=__cli_paste_board)

    parser_fi = subparsers.add_parser('fi', help="matti file mode")
    parser_fi.add_argument('srcpath', nargs='?', default='.', help="check raw directry.")
    parser_fi.add_argument('-i', '--input', nargs='?', help='search jpg directry.')
    parser_fi.set_defaults(handler=__cli_file)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
