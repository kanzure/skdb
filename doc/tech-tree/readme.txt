I spent over a day writing a silly Python program to read in a Civilization 2 Technology Tree.

I learned:

    * Python assert statements tend to fail silently during common misuse. Blogged about it. Suggested fixing it on the Py3k mailing list. Guido says there is a SyntaxWarning now.
    * Google docs appears to use the python csv module to export to csv. Their spreadsheet works fairly well. I like the auto-save/auto-versioning.
    * The csv package is pretty inflexible. It cannot discover the dialect of comma-separated-vague file it is passed. It works for, and is designed for, times when the export is either excel or Python. The Dialects do allow you to set some other basic options.
    * nose is a great testing tool. nose.tools confuses pylint because of its on-the-fly playing with __all__. I should probably write a Wikipedia article on it.
    * Whenever debugging recursion, make a note both when calling the recursed function and when returning. It makes digging through the log much easier.
    * Nothing tests your code like a large, real world, example.
    * The logging function rocks far less well. I filed bug on it: it picks up the wrong %(filename)s. This bug has apparently been going back and forth for years.
    * Reading a correctly validated input file is about 10x the effort of reading an incorrectly validated one.
    * Testing code is fairly easy and a bit bulky. It’s real cost is that it forces that 10x effort in validating the input in order to pass the tests. I could get behind Test Driven Development.
    * The Civilization 2 Technology Tree has five errors, including two “Destroyer” units and a bunch of redundant dependencies, such as Fusion Power doesn’t need to depend on Nuclear Power.
    * Sets in Python work well.
    * WordPress has syntax coloring plug-ins that work fairly well, and it can handle arbitrary files.
    * Programming is still fun.

So, with no plans to do anything with this:

tech.py — This is Python code. It loads the technology tree and doesn’t do anything with it.

civtech.csv — A CSV file with the Civilization 2 technology tree

CivChart — A GoogleDoc spreadsheet with that same technology tree
