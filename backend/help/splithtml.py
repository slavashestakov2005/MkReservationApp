import re
import os


class FilePart:
    def __init__(self, text, is_comment=False):
        self.text = text
        self.is_comment = is_comment


class SplitFile:
    def read_file(self):
        with open(self.file_name, 'r', encoding='UTF-8') as f:
            data = f.read()
        return re.split(r'(<!--|-->)', data)

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.parts = []
        self.replace = {}
        self.edited = False
        is_comment = False
        parts = self.read_file()
        for part in parts:
            if part == '<!--':
                is_comment = True
            elif part == '-->':
                is_comment = False
            else:
                self.parts.append(FilePart(part, is_comment))

    def insert_after_comment(self, comment: str, text: str, is_comment: bool = False, append: bool = False):
        for index in range(len(self.parts)):
            if self.parts[index].is_comment and self.parts[index].text == comment:
                self.edited = True
                if not self.parts[index + 1].is_comment:
                    if not append:
                        self.parts[index + 1] = FilePart(text, is_comment)
                    else:
                        self.parts[index + 1] = FilePart(self.parts[index + 1].text + text, is_comment)
                else:
                    self.parts.insert(index + 1, FilePart(text))

    def replace_comment(self, comment: str, text: str):
        for index in range(len(self.parts)):
            if self.parts[index].is_comment and self.parts[index].text == comment:
                self.edited = True
                self.replace[index] = text

    def writable(self) -> str:
        result = ''
        index = 0
        for part in self.parts:
            if index in self.replace:
                result += self.replace[index]
            else:
                if part.is_comment:
                    result += '<!--'
                result += part.text
                if part.is_comment:
                    result += '-->'
            index += 1
        return result

    def save_file(self, file_name=None):
        if not file_name:
            file_name = self.file_name
        if self.edited:
            if not os.path.exists(os.path.dirname(file_name)):
                os.makedirs(os.path.dirname(file_name))
            with open(file_name, 'w', encoding='UTF-8') as f:
                f.write(self.writable())
        self.replace = {}
