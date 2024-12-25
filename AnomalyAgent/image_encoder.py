import base64
import logging

def encode_image(image_path):
    """
    Encode an image file to a dictionary containing mime_type and Base64 data.
    
    Parameters:
    - image_path: The path to the image file.
    
    Returns:
    - A dictionary with 'mime_type' and 'data' keys.
    """
    try:
        with open(image_path, "rb") as img_file:
            img_bytes = img_file.read()

        # Base64 encode the image data
        img_b64 = base64.b64encode(img_bytes).decode('utf-8')

        # Define the mime type (you can adjust it for PNG or other formats if needed)
        mime_type = "image/jpeg"  # Change this if the image is in another format (e.g., 'image/png')

        # Return the dictionary containing mime_type and the Base64 data
        return {
            "mime_type": mime_type,
            "data": img_b64
        }
    
    except Exception as e:
        logging.error(f"Failed to encode image {image_path}: {e}")
        raise e
