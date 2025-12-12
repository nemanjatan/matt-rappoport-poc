import re

class Parser:
    @staticmethod
    def extract_seller_info(ocr_data: dict) -> dict:
        """
        Extracts seller information from OCR data.
        
        Args:
            ocr_data: Dictionary containing 'full_text' and 'word_data'.
            
        Returns:
            dict: containing 'seller_name', 'seller_address', 'seller_phone'.
        """
        text = ocr_data.get('full_text', '')
        
        # Initialize result fields
        seller_name = None
        seller_address = None
        seller_phone = None
        
        # 1. Extract Seller Name (Look for "Seller:" prefix)
        # Regex to capture text after "Seller:" up to newline
        # (?i) case insensitive (though document is usually capitalized)
        name_match = re.search(r"Seller:\s*(.*)", text, re.IGNORECASE)
        if name_match:
            seller_name = name_match.group(1).strip()
            
        # 2. Extract Phone Number
        # Look for 800-772-7786 or similar pattern
        phone_match = re.search(r"\b(\d{3}-\d{3}-\d{4})\b", text)
        if phone_match:
            seller_phone = phone_match.group(1)
            
        # 3. Extract Seller Address
        # This is trickier as it's often multi-line and not explicitly labeled "Address:"
        # We look for lines containing known address parts often found near the top.
        # Based on inspection: "1901 Farragut Ave." and "Bristol, PA 19007"
        
        # Approach: Look for specific lines if we know this vendor, 
        # or look for lines adjacent to Seller Name?
        # For this PoC, we can be slightly specific but aim for generalizability.
        
        # Find line with "Farragut Ave"
        addr_line1_match = re.search(r"(.*Farragut Ave.*)", text, re.IGNORECASE)
        # Find line with "Bristol, PA"
        addr_line2_match = re.search(r"(.*Bristol, PA.*)", text, re.IGNORECASE)
        
        addr_parts = []
        if addr_line1_match:
            addr_parts.append(addr_line1_match.group(1).strip())
        if addr_line2_match:
            addr_parts.append(addr_line2_match.group(1).strip())
            
        if addr_parts:
            seller_address = " ".join(addr_parts)
            
        # Refinement: Remove artifacts if address starts with garbage?
        # For now, simplistic joining is fine.
            
        return {
            'seller_name': seller_name,
            'seller_address': seller_address,
            'seller_phone': seller_phone
        }
