"""
UGOS Confirmation Gates
Handles user confirmation for write operations per UGOS requirements.
"""

from typing import List, Dict, Any, Optional
import sys


class UGOSConfirmation:
    """Handles UGOS-mandated user confirmations for write operations."""
    
    @staticmethod
    def confirm_single(message: str, test_mode: bool = False) -> bool:
        """
        Single confirmation prompt for operations like generating briefing.
    
        Args:
            message: Confirmation message to display
            test_mode: If True, auto-confirm without prompting
    
        Returns:
            True if user confirms, False otherwise
        """
        if test_mode:
            print(f"\n{'='*60}")
            print(f"⚠️  UGOS CONFIRMATION REQUIRED (TEST MODE: AUTO-CONFIRM)")
            print(f"{'='*60}")
            print(f"{message}")
            print(f"{'='*60}")
            print("[AUTO-CONFIRMED] Proceeding with operation...")
            return True
    
        print(f"\n{'='*60}")
        print(f"⚠️  UGOS CONFIRMATION REQUIRED")
        print(f"{'='*60}")
        print(f"{message}")
        print(f"{'='*60}")
    
        while True:
            response = input("Confirm? [y/N]: ").strip().lower()
            if response in ('y', 'yes'):
                print("[CONFIRMED] Proceeding with operation...")
                return True
            elif response in ('n', 'no', ''):
                print("[CANCELLED] Operation cancelled by user.")
                return False
            else:
                print("Please enter 'y' or 'n'")
    
    @staticmethod
    def confirm_batch(message: str, items: Optional[List[Any]] = None, test_mode: bool = False) -> bool:
        """
        Batch confirmation for multiple items (e.g., multiple clip extractions).
        
        Args:
            message: Confirmation message
            items: Optional list of items being confirmed
            test_mode: If True, auto-confirm without prompting
        
        Returns:
            True if user confirms, False otherwise
        """
        if test_mode:
            print(f"\n{'='*60}")
            print(f"⚠️  UGOS BATCH CONFIRMATION REQUIRED (TEST MODE: AUTO-CONFIRM)")
            print(f"{'='*60}")
            print(f"{message}")
            
            if items:
                print(f"\nItems ({len(items)}):")
                for i, item in enumerate(items[:10]):
                    print(f"  {i+1}. {item}")
                if len(items) > 10:
                    print(f"  ... and {len(items) - 10} more items")
            
            print(f"{'='*60}")
            print("[AUTO-CONFIRMED] Proceeding with batch operation...")
            return True
        
        print(f"\n{'='*60}")
        print(f"⚠️  UGOS BATCH CONFIRMATION REQUIRED")
        print(f"{'='*60}")
        print(f"{message}")
        
        if items:
            print(f"\nItems ({len(items)}):")
            for i, item in enumerate(items[:10]):
                print(f"  {i+1}. {item}")
            if len(items) > 10:
                print(f"  ... and {len(items) - 10} more items")
        
        print(f"{'='*60}")
        
        while True:
            response = input("Confirm all? [y/N]: ").strip().lower()
            if response in ('y', 'yes'):
                print("[CONFIRMED] Proceeding with batch operation...")
                return True
            elif response in ('n', 'no', ''):
                print("[CANCELLED] Batch operation cancelled by user.")
                return False
            else:
                print("Please enter 'y' or 'n'")


# Convenience functions for direct import
def confirm_single(message: str, test_mode: bool = False) -> bool:
    """Convenience function for single confirmation."""
    return UGOSConfirmation.confirm_single(message, test_mode)


def confirm_batch(message: str, items: Optional[List[Any]] = None, test_mode: bool = False) -> bool:
    """Convenience function for batch confirmation."""
    return UGOSConfirmation.confirm_batch(message, items, test_mode)


# For testing
if __name__ == "__main__":
    # Test single
    result = confirm_single("Generate HTML security briefing?")
    print(f"Result: {result}")
    
    # Test batch
    test_items = [
        "Clip 1: cam-front person 14:32",
        "Clip 2: cam-garage vehicle 16:15",
        "Clip 3: cam-backyard motion 18:44"
    ]
    result = confirm_batch("Extract 3 clips?", test_items)
    print(f"Result: {result}")