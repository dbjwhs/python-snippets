# MIT License
# Copyright (c) 2025 dbjwhs

"""
Example of creating a custom chain of responsibility for document approval.

This example demonstrates how to extend the Chain of Responsibility pattern
for a different use case (document approval) while using the same basic pattern.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional

from src.chain_of_responsibility.logger import Logger, LogLevel


class DocumentType(Enum):
    """Types of documents that can be approved."""
    
    INTERNAL_MEMO = auto()
    CONTRACT = auto()
    PRESS_RELEASE = auto()
    FINANCIAL_REPORT = auto()


@dataclass
class Document:
    """A document that needs approval."""
    
    title: str
    content: str
    doc_type: DocumentType
    author: str
    word_count: int


class DocumentApprover:
    """Base class for document approvers in the chain."""
    
    def __init__(self, position: str) -> None:
        """Initialize a document approver.
        
        Args:
            position: The approver's position/role in the organization
        """
        self._position = position
        self._next_approver: Optional[DocumentApprover] = None
        self._logger = Logger.get_instance()
    
    def set_next(self, approver: "DocumentApprover") -> "DocumentApprover":
        """Set the next approver in the chain.
        
        Args:
            approver: The next approver
            
        Returns:
            The next approver for method chaining
        """
        self._next_approver = approver
        return approver
    
    def process_document(self, document: Document) -> bool:
        """Process a document approval request.
        
        Args:
            document: The document to approve
            
        Returns:
            True if approved, False otherwise
        """
        if self.can_approve(document):
            self._approve_document(document)
            return True
        elif self._next_approver:
            self._logger.log(
                LogLevel.INFO,
                f"{self._position} cannot approve this document. Forwarding to next approver."
            )
            return self._next_approver.process_document(document)
        else:
            self._logger.log(
                LogLevel.INFO,
                f"Document '{document.title}' could not be approved by any approver in the chain."
            )
            return False
    
    def can_approve(self, document: Document) -> bool:
        """Determine if this approver can approve the document.
        
        Args:
            document: The document to check
            
        Returns:
            True if this approver can approve the document
        """
        return False  # Base implementation always forwards
    
    def _approve_document(self, document: Document) -> None:
        """Approve the document.
        
        Args:
            document: The document to approve
        """
        self._logger.log(
            LogLevel.INFO,
            f"{self._position} has approved document: '{document.title}'"
        )


class TeamLead(DocumentApprover):
    """Team lead can approve internal memos."""
    
    def __init__(self) -> None:
        """Initialize a team lead approver."""
        super().__init__("Team Lead")
    
    def can_approve(self, document: Document) -> bool:
        """Team leads can only approve internal memos under 1000 words.
        
        Args:
            document: The document to check
            
        Returns:
            True if it's an internal memo under 1000 words
        """
        return (
            document.doc_type == DocumentType.INTERNAL_MEMO and 
            document.word_count < 1000
        )


class Manager(DocumentApprover):
    """Manager can approve internal memos and small contracts."""
    
    def __init__(self) -> None:
        """Initialize a manager approver."""
        super().__init__("Department Manager")
    
    def can_approve(self, document: Document) -> bool:
        """Managers can approve internal memos and contracts under 2000 words.
        
        Args:
            document: The document to check
            
        Returns:
            True if it's an approvable document
        """
        if document.doc_type == DocumentType.INTERNAL_MEMO:
            return True
        if document.doc_type == DocumentType.CONTRACT and document.word_count < 2000:
            return True
        return False


class Director(DocumentApprover):
    """Director can approve most documents except financial reports."""
    
    def __init__(self) -> None:
        """Initialize a director approver."""
        super().__init__("Director")
    
    def can_approve(self, document: Document) -> bool:
        """Directors can approve most document types except financial reports.
        
        Args:
            document: The document to check
            
        Returns:
            True if it's an approvable document
        """
        return document.doc_type != DocumentType.FINANCIAL_REPORT


class CEO(DocumentApprover):
    """CEO can approve any document."""
    
    def __init__(self) -> None:
        """Initialize a CEO approver."""
        super().__init__("CEO")
    
    def can_approve(self, document: Document) -> bool:
        """CEOs can approve any document.
        
        Args:
            document: The document to check
            
        Returns:
            Always True
        """
        return True


def main() -> None:
    """Run the document approval example."""
    logger = Logger.get_instance()
    logger.log(LogLevel.INFO, "Document Approval Chain of Responsibility Example")
    logger.log(LogLevel.INFO, "-------------------------------------------")
    
    # Create the chain
    team_lead = TeamLead()
    manager = Manager()
    director = Director()
    ceo = CEO()
    
    team_lead.set_next(manager)
    manager.set_next(director)
    director.set_next(ceo)
    
    # Create some sample documents
    documents: List[Document] = [
        Document(
            "Team Meeting Notes", 
            "Notes from the team meeting...", 
            DocumentType.INTERNAL_MEMO, 
            "John Smith", 
            500
        ),
        Document(
            "Vendor Agreement", 
            "Terms for the new vendor...", 
            DocumentType.CONTRACT, 
            "Jane Doe", 
            1500
        ),
        Document(
            "New Product Announcement", 
            "Press release for the new product...", 
            DocumentType.PRESS_RELEASE, 
            "Marketing Team", 
            800
        ),
        Document(
            "Q2 Financial Summary", 
            "Financial report for Q2...", 
            DocumentType.FINANCIAL_REPORT, 
            "Accounting Dept", 
            3000
        ),
    ]
    
    # Process each document
    for doc in documents:
        logger.log(LogLevel.INFO, f"Processing document: '{doc.title}' ({doc.doc_type.name})")
        approved = team_lead.process_document(doc)
        result = "APPROVED" if approved else "REJECTED"
        logger.log(LogLevel.INFO, f"Document status: {result}")
        logger.log(LogLevel.INFO, "-------------------------------------------")


if __name__ == "__main__":
    main()