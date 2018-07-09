# This software includes the work that is distributed in the Apache License 2.0

import glob

import wx
from bs4 import BeautifulSoup
from fontTools.subset import Options, Subsetter, load_font, save_font


class MyApp(wx.Frame):

    def __init__(self, *args, **kw):
        super(MyApp, self).__init__(*args, **kw)

        self.init_ui()
        self.Show()

    def init_ui(self):
        self.SetTitle('Font Subsetter')
        self.SetSize((600, 480))

        fonts = [font.split('/')[-1] for font in glob.glob('./fonts/*.otf')]

        wx.StaticText(self, -1, 'フォント選択', pos=(10, 10))
        self.combobox = wx.ComboBox(self, -1, 'フォント選択してください', choices=fonts,
                                    pos=(10, 30), size=(280, 25))

        wx.StaticText(self, -1, '出力ファイル名', pos=(310, 10))
        self.box_name = wx.TextCtrl(self, -1, pos=(310, 30), size=(280, 25))

        wx.StaticText(self, -1, '出力フォルダ', pos=(10, 80))
        btn_out = wx.Button(self, -1, 'フォルダを選択', pos=(10, 100))
        btn_out.Bind(wx.EVT_BUTTON, self.select_folder)
        self.box_out = wx.TextCtrl(self, -1, pos=(10, 125), size=(580, 25))

        wx.StaticText(self, -1, 'サブセット', pos=(10, 180))
        notebook = wx.Notebook(self, -1, pos=(10, 200), size=(580, 250))
        pnl_text = wx.Panel(notebook, -1)
        pnl_file = wx.Panel(notebook, -1)
        pnl_html = wx.Panel(notebook, -1)
        notebook.InsertPage(0, pnl_text, "テキストから")
        notebook.InsertPage(1, pnl_file, "ファイルから")
        notebook.InsertPage(2, pnl_html, "HTMLから")

        self.box_text = wx.TextCtrl(
            pnl_text, -1, pos=(10, 10), size=(540, 150))
        btn_gen_text = wx.Button(pnl_text, -1, '作成', pos=(265, 170),
                                 size=(50, 25))
        btn_gen_text.Bind(wx.EVT_BUTTON, self.subset_font_text)

        btn_file = wx.Button(pnl_file, -1, 'ファイルを選択', pos=(10, 10))
        btn_file.Bind(wx.EVT_BUTTON, self.select_file)
        self.box_file = wx.TextCtrl(pnl_file, -1, pos=(10, 40), size=(540, 25))
        btn_gen_file = wx.Button(pnl_file, -1, '作成', pos=(265, 170),
                                 size=(50, 25))
        btn_gen_file.Bind(wx.EVT_BUTTON, self.subset_font_file)

        btn_html = wx.Button(pnl_html, -1, 'ファイルを選択', pos=(10, 10))
        btn_html.Bind(wx.EVT_BUTTON, self.select_html)
        self.box_html = wx.TextCtrl(pnl_html, -1, pos=(10, 40), size=(540, 25))
        btn_gen_html = wx.Button(pnl_html, -1, '作成', pos=(265, 170),
                                 size=(50, 25))
        btn_gen_html.Bind(wx.EVT_BUTTON, self.subset_font_html)

    def select_folder(self, event):
        dialog = wx.DirDialog(None, 'フォルダを選択してください')
        dialog.ShowModal()
        self.box_out.SetValue(dialog.GetPath())

    def select_file(self, event):
        dialog = wx.FileDialog(None, 'ファイルを選択してください')
        dialog.ShowModal()
        self.box_file.SetValue(dialog.GetPath())

    def select_html(self, event):
        dialog = wx.FileDialog(None, 'ファイルを選択してください')
        dialog.ShowModal()
        self.box_html.SetValue(dialog.GetPath())

    def subset_font(self, text):
        if (self.box_out.GetValue() != '') & (self.box_name.GetValue() != '') & (self.combobox.GetValue() != ''):
            path = '{}/{}'.format(self.box_out.GetValue(),
                                  self.box_name.GetValue())
            for flavor in ['otf', 'woff', 'woff2']:
                options = Options()
                if flavor != 'otf':
                    options.flavor = flavor
                font = load_font(
                    './fonts/{}'.format(self.combobox.GetValue()), options)
                subsetter = Subsetter(options=options)
                subsetter.populate(text=text)
                subsetter.subset(font)
                save_font(font, '{}.{}'.format(path, flavor), options)
                font.close()
            dialog = wx.MessageDialog(
                self, '生成終了', 'Font Subsetter', style=wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        else:
            dialog = wx.MessageDialog(
                self, '生成失敗:空欄があります', 'Font Subsetter', style=wx.OK)
            dialog.ShowModal()
            dialog.Destroy()

    def subset_font_text(self, event):
        text = self.box_text.GetValue().replace(
            '\n', '').replace('\r', '').replace('\t', '')
        self.subset_font(text)

    def subset_font_file(self, event):
        with open(self.box_file.GetValue()) as f:
            text = f.read()
        text = text.replace('\n', '').replace('\r', '').replace('\t', '')
        self.subset_font(text)

    def subset_font_html(self, event):
        with open(self.box_html.GetValue()) as f:
            html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.body.get_text().replace('\n', '').replace('\r', '').replace('\t', '')
        self.subset_font(text)


app = wx.App()
MyApp(None)
app.MainLoop()
