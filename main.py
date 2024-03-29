from markdown.writer import *


if __name__ == '__main__':
    writer = MarkdownWriter()
    writer.addHeading("Hello, World!", 1)
    writer.addText("This is a test.")
    writer.addHorizontalRule()
    writer.addText("This is another test.")
    writer.addLink("https://example.com", "Example")
    writer.addImage("https://example.com/image.png", "Image")
    writer.addCodeBlock("print('Hello, World!')", 'python')
    writer.addBlockquote("This is a blockquote.")
    writer.addBold("This is bold.")
    writer.addItalic("This is italic.")
    writer.addLineBreak()
    writer.addFrontMatter({'title': 'Hello, World!'})
    writer.addList(['One', 'Two', 'Three'])
    writer.addOrderedList(['One', 'Two', 'Three'])
    writer.addTable(['One', 'Two', 'Three'], [['1', '2', '3'], ['4', '5', '6']])
    writer.addAdmonition("Hello, World!", "This is an admonition.")
    writer.addBlock("Hello", "World", "This is a block.")
    writer.addHtmlBlock("div", "Hello, World!")
    writer.addTab("Hello", "World")
    writer.addDefinitionList({'One': '1', 'Two': '2', 'Three': '3'})
    writer.addAnnotation("Hello, World!", ["This is an annotation."])
    writer.addSymbol("Hello, World!")
    print(writer.render())

