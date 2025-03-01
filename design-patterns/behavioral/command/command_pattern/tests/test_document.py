"""
Tests for the document editing functionality of the Command pattern.
"""


from command_pattern.command import (
    Document,
    DocumentEditor,
    EraseCommand,
    InsertCommand,
)


def test_document_initialization() -> None:
    """Test that a document is initialized with empty content."""
    doc = Document()
    assert doc.content == ""


def test_document_insert() -> None:
    """Test the insert operation on a document."""
    doc = Document()
    doc.insert("Hello", 0)
    assert doc.content == "Hello"

    doc.insert(" World", 5)
    assert doc.content == "Hello World"

    doc.insert("Python ", 0)
    assert doc.content == "Python Hello World"


def test_document_erase() -> None:
    """Test the erase operation on a document."""
    doc = Document("Hello World")
    doc.erase(5, 6)  # Erase " World"
    assert doc.content == "Hello"

    doc = Document("Python")
    doc.erase(0, 6)  # Erase everything
    assert doc.content == ""


def test_insert_command() -> None:
    """Test the InsertCommand class."""
    doc = Document()
    cmd = InsertCommand(doc, "Hello", 0)
    cmd.execute()
    assert doc.content == "Hello"

    # Test undo
    cmd.undo()
    assert doc.content == ""

    # Test re-execute
    cmd.execute()
    assert doc.content == "Hello"


def test_erase_command() -> None:
    """Test the EraseCommand class."""
    doc = Document("Hello World")
    cmd = EraseCommand(doc, 6, 5)  # Erase "World"
    cmd.execute()
    assert doc.content == "Hello "

    # Test undo
    cmd.undo()
    assert doc.content == "Hello World"

    # Test re-execute
    cmd.execute()
    assert doc.content == "Hello "


def test_document_editor() -> None:
    """Test the DocumentEditor class functionality."""
    doc = Document()
    editor = DocumentEditor(doc)

    # Test insert
    editor.execute_command(InsertCommand(doc, "Hello", 0))
    assert doc.content == "Hello"

    # Test erase
    editor.execute_command(EraseCommand(doc, 0, 2))
    assert doc.content == "llo"

    # Test undo
    editor.undo()
    assert doc.content == "Hello"

    # Test redo
    editor.redo()
    assert doc.content == "llo"

    # Test multiple commands
    editor.execute_command(InsertCommand(doc, " World", 3))
    assert doc.content == "llo World"
    editor.execute_command(EraseCommand(doc, 3, 1))  # Erase the space
    assert doc.content == "lloWorld"

    # Test multiple undos
    editor.undo()  # Undo last erase
    assert doc.content == "llo World"
    editor.undo()  # Undo last insert
    assert doc.content == "llo"
    editor.undo()  # Undo first erase
    assert doc.content == "Hello"

    # Test redo after multiple undos
    editor.redo()  # Redo first erase
    assert doc.content == "llo"

    # Test that executing a new command clears redo stack
    editor.execute_command(InsertCommand(doc, "XYZ", 0))
    assert doc.content == "XYZllo"
    # Now redo should do nothing
    editor.redo()
    assert doc.content == "XYZllo"


def test_command_cloning() -> None:
    """Test the clone method of commands."""
    doc = Document("Hello")
    
    # Test InsertCommand cloning
    insert_cmd = InsertCommand(doc, " World", 5)
    insert_clone = insert_cmd.clone()
    insert_clone.execute()
    assert doc.content == "Hello World"
    insert_clone.undo()
    assert doc.content == "Hello"
    
    # Test EraseCommand cloning
    erase_cmd = EraseCommand(doc, 0, 5)
    erase_clone = erase_cmd.clone()
    erase_clone.execute()
    assert doc.content == ""
    erase_clone.undo()
    assert doc.content == "Hello"