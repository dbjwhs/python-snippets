"""
Example usage of the command pattern for document editing.

This example demonstrates how to use the command pattern to implement
a simple text editor with undo/redo functionality.
"""

from icecream import ic

from command_pattern.command import (
    Document,
    DocumentEditor,
    EraseCommand,
    InsertCommand,
)


def main() -> None:
    """Run the document editing example."""
    # Configure icecream
    ic.configureOutput(prefix="[Document Example] ")
    
    # Create a document and editor
    doc = Document()
    editor = DocumentEditor(doc)
    
    ic("Command Pattern - Document Editing Example")
    ic("------------------------------------------")
    ic("Initial document content: ''")
    
    # Insert some text
    ic("Inserting text 'Hello, world!'...")
    editor.execute_command(InsertCommand(doc, "Hello, world!", 0))
    ic(f"Document content: '{doc.content}'")
    
    # Erase some text
    ic("Erasing 'world'...")
    editor.execute_command(EraseCommand(doc, 7, 5))
    ic(f"Document content: '{doc.content}'")
    
    # Insert more text
    ic("Inserting 'Python'...")
    editor.execute_command(InsertCommand(doc, "Python", 7))
    ic(f"Document content: '{doc.content}'")
    
    # Demonstrate undo
    ic("Undo (remove 'Python')...")
    editor.undo()
    ic(f"Document content: '{doc.content}'")
    
    ic("Undo (restore 'world')...")
    editor.undo()
    ic(f"Document content: '{doc.content}'")
    
    # Demonstrate redo
    ic("Redo (erase 'world')...")
    editor.redo()
    ic(f"Document content: '{doc.content}'")
    
    # Insert different text
    ic("Inserting 'Command Pattern'...")
    editor.execute_command(InsertCommand(doc, "Command Pattern", 7))
    ic(f"Document content: '{doc.content}'")
    
    # Note: redo stack is now cleared because we executed a new command
    ic("NOTE: The redo stack is now cleared because we executed a new command.")
    
    # Undo again to demonstrate we can still undo
    ic("Undo (remove 'Command Pattern')...")
    editor.undo()
    ic(f"Document content: '{doc.content}'")
    
    ic("Undo (restore 'world')...")
    editor.undo()
    ic(f"Document content: '{doc.content}'")
    
    ic("Document editing operations completed.")


if __name__ == "__main__":
    main()