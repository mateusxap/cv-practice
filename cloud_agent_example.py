"""
Example: Delegating Image Processing to Cloud Agent

This module demonstrates the concept of delegating compute-intensive
image processing tasks to a cloud agent/service.
"""

import cv2
import numpy as np
from typing import Optional, Tuple


class CloudAgentDelegate:
    """
    A delegate class that shows how to structure code for cloud-based processing.
    
    In a real implementation, this would connect to a cloud service API
    for distributed image processing.
    """
    
    def __init__(self, endpoint: Optional[str] = None):
        """
        Initialize the cloud agent delegate.
        
        Args:
            endpoint: Optional cloud service endpoint URL
        """
        self.endpoint = endpoint or "http://localhost:8000"
        self.connected = False
    
    def connect(self) -> bool:
        """
        Establish connection to cloud agent.
        
        Returns:
            True if connection successful, False otherwise
        """
        # In real implementation, this would connect to actual cloud service
        print(f"Connecting to cloud agent at {self.endpoint}...")
        self.connected = True
        return self.connected
    
    def process_image_remote(self, image: np.ndarray, operation: str, 
                            **kwargs) -> np.ndarray:
        """
        Delegate image processing to cloud agent.
        
        Args:
            image: Input image as numpy array
            operation: Processing operation name (e.g., 'sepia', 'blur', 'resize')
            **kwargs: Additional operation parameters
            
        Returns:
            Processed image as numpy array
        """
        if not self.connected:
            raise RuntimeError("Not connected to cloud agent. Call connect() first.")
        
        # In real implementation, this would:
        # 1. Serialize the image
        # 2. Send to cloud service via HTTP/gRPC
        # 3. Receive processed result
        # 4. Deserialize and return
        
        print(f"Delegating {operation} operation to cloud agent...")
        
        # For demonstration, perform operation locally
        if operation == 'sepia':
            return self._apply_sepia_local(image)
        elif operation == 'resize':
            target_size = kwargs.get('size', (800, 600))
            return cv2.resize(image, target_size)
        elif operation == 'blur':
            kernel_size = kwargs.get('kernel_size', 15)
            return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        else:
            return image
    
    def _apply_sepia_local(self, image: np.ndarray) -> np.ndarray:
        """
        Apply sepia effect (local fallback).
        
        Args:
            image: Input image
            
        Returns:
            Sepia-toned image
        """
        kernel = np.array([[0.272, 0.534, 0.131],
                          [0.349, 0.686, 0.168],
                          [0.393, 0.769, 0.189]])
        
        sepia = cv2.transform(image, kernel)
        sepia = np.clip(sepia, 0, 255).astype(np.uint8)
        return sepia
    
    def disconnect(self):
        """Disconnect from cloud agent."""
        print("Disconnecting from cloud agent...")
        self.connected = False


def main():
    """
    Demonstrate cloud agent delegation for image processing.
    """
    # Create a sample image
    image = np.zeros((400, 600, 3), dtype=np.uint8)
    image[:] = (100, 150, 200)  # Fill with a color
    
    # Initialize cloud delegate
    delegate = CloudAgentDelegate()
    delegate.connect()
    
    # Delegate processing tasks
    try:
        # Apply sepia effect via cloud agent
        sepia_image = delegate.process_image_remote(image, 'sepia')
        print("✓ Sepia effect applied via cloud agent")
        
        # Apply blur via cloud agent
        blurred = delegate.process_image_remote(image, 'blur', kernel_size=21)
        print("✓ Blur applied via cloud agent")
        
        # Resize via cloud agent
        resized = delegate.process_image_remote(image, 'resize', 
                                               size=(300, 200))
        print("✓ Resize applied via cloud agent")
        
        print("\nAll operations delegated successfully!")
        
    finally:
        delegate.disconnect()


if __name__ == "__main__":
    main()
