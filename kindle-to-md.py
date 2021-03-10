import re
import os
def process (clippings):
    if not os.path.isfile(clippings):
        print("Can't find file My Clippings.txt in current directory, pls add it!")
        exit()
    books = {}
    authors = {}
    words = []
    # reset values
    title = None
    author = None
    quote = None
    pgnumber = None
    datestr = None
    metadata = None
    with open(clippings, "r") as f:
        new_book = True
        marking = "=========="
        for line in f:
            line = line.strip()
            if marking in line:
                new_book = True
                # reset values
                title = None
                author = None
                quote = None
                pgnumber = None
                datestr = None
                metadata = None
                continue
            elif new_book: # match title and author
                new_book = False
                # format is typically 'Deschooling Society (Ivan Illich)\r\n'
                match = re.match(r"^(.*)\s+\((.*)\)", line)
                if match:
                    title = match.group(1)
                    author = match.group(2)
                    if author is None or author == "None" or len(author.strip()) == 0: 
                        author = "Unknown"
            elif re.match(r"^-[Highlight on Page|Bookmark on | Highlight Loc.]", line):
                metadata = line
            elif metadata and line != "\n":
                if not title in books: 
                    books[title] = list()
                if not author in authors: 
                    authors[author] = dict()
                if not title in authors[author]:
                    authors[author][title] = list()
                if line.count(" ") == 0 and len(line) > 0: 
                    words.append(re.sub(r"[.,!?:;]", "", line).lower())
                    continue
                authors[author][title].append(line)
                books[title].append({ "author": author, "quote": line })
        with open("./books.md", "w") as f:
            print("Writing books.md")
            for book in books:
                title = book if book else ""
                f.write("* {}\n".format(title))
            f.write("\n")
            for book in books:
                title = book if book else ""
                f.write("# {}\n".format(title))
                for saved in books[book]:
                    f.write("> {}\n".format(saved["quote"]))
        with open("./authors.md", "w") as f:
            print("Writing authors.md")
            for author in authors:
                f.write("* {}\n".format(author))
            f.write("\n")
            for author in authors:
                f.write("# {}\n".format(author))
                for book in authors[author]:
                    f.write("#### {}\n".format(book))
                    for quote in authors[author][book]:
                        f.write(quote + "\n")
        with open ("./words.md", "w") as f:
            print("Writing words.md")
            for word in words:
                f.write("{}\n".format(word))


# format
#
# <book title> (<author>)
# - [Bookmark|Highlight] on Page (<number>) | Highlight Loc. <number> | Added on <date string>
# ==========

process("My Clippings.txt")
