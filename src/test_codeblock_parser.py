from parsed_codeblock import ParsedCodeBlock
from codeblock_parser import CodeblockParser

from utils import split_lines_using_anki_separator

def test_parsing_of_one_codeblock():
    parser = CodeblockParser()

    content = '''
    ```anki
        some code
        some more code
    ```
    '''

    codeblocks = parser.parse_text(content, None)

    assert len(codeblocks) == 1

    codeblock: ParsedCodeBlock = codeblocks[0]

    assert codeblock.type == "anki"

    codeblock_content = split_lines_using_anki_separator(codeblock.content)

    assert len(codeblock_content) == 2
    assert codeblock_content[0].strip() == "some code"
    assert codeblock_content[1].strip() == "some more code"

def test_parsing_of_one_markdown_codeblock():
    parser = CodeblockParser()

    content = '''
    ```markdown anki
        some code
        some more code
    ```
    '''

    codeblocks = parser.parse_text(content, None)

    assert len(codeblocks) == 1

    codeblock: ParsedCodeBlock = codeblocks[0]

    assert codeblock.type == "markdown"

    codeblock_content = split_lines_using_anki_separator(codeblock.content)

    assert len(codeblock_content) == 2
    assert codeblock_content[0].strip() == "some code"
    assert codeblock_content[1].strip() == "some more code"


def test_ignoring_of_one_markdown_codeblock_without_anki_annotation():
    parser = CodeblockParser()

    # note no `anki`
    content = '''
    ```markdown
        some code
        some more code
    ```
    '''

    codeblocks = parser.parse_text(content, None)

    assert len(codeblocks) == 0


def test_parsing_of_headers_one_codeblock():
    parser = CodeblockParser()

    content = '''
    ```markdown anki header1:value header2
        some code
        some more code
    ```
    '''

    codeblocks = parser.parse_text(content, None)

    assert len(codeblocks) == 1

    codeblock: ParsedCodeBlock = codeblocks[0]

    assert codeblock.type == "markdown"

    assert len(codeblock.headers) == 3
    assert codeblock.headers[0] == "anki"
    assert codeblock.headers[1] == "header1:value"
    assert codeblock.headers[2] == "header2"

def test_parsing_of_multiple_codeblocks():
    parser = CodeblockParser()

    content = '''
    ```anki
        some code
        some more code
    ```

    some irrelevant text
    some irrelevant text
    some irrelevant text

    ```markdown anki
        some code2
        some more code2
    ```

    some irrelevant text
    some irrelevant text

    ```anki
        some code3
        some more code3
        some more more code3
    ```
    '''

    codeblocks = parser.parse_text(content, None)

    assert len(codeblocks) == 3

    codeblock1: ParsedCodeBlock = codeblocks[0]
    codeblock2: ParsedCodeBlock = codeblocks[1]
    codeblock3: ParsedCodeBlock = codeblocks[2]

    assert codeblock1.type == "anki"
    assert codeblock2.type == "markdown"
    assert codeblock3.type == "anki"

    codeblock1_content = split_lines_using_anki_separator(codeblock1.content)
    codeblock2_content = split_lines_using_anki_separator(codeblock2.content)
    codeblock3_content = split_lines_using_anki_separator(codeblock3.content)

    assert len(codeblock1_content) == 2
    assert codeblock1_content[0].strip() == "some code"
    assert codeblock1_content[1].strip() == "some more code"

    assert len(codeblock2_content) == 2
    assert codeblock2_content[0].strip() == "some code2"
    assert codeblock2_content[1].strip() == "some more code2"


    assert len(codeblock3_content) == 3
    assert codeblock3_content[0].strip() == "some code3"
    assert codeblock3_content[1].strip() == "some more code3"
    assert codeblock3_content[2].strip() == "some more more code3"