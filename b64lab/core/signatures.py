"""
Magic Byte File Signature Engine & Payload Classifier.
Pure Python standard library implementation.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple

@dataclass
class FileSignature:
    """Represents a recognized file signature pattern."""
    category: str
    extension: str
    mime_type: str
    description: str
    magic_bytes: bytes
    offset: int = 0

class SignatureDB:
    """
    Security-focused magic byte signature database.
    Used by incident responders to identify carved payloads.
    """

    SIGNATURES: List[FileSignature] = [
        # Executables & Binaries
        FileSignature(
            category="EXECUTABLE",
            extension="exe",
            mime_type="application/vnd.microsoft.portable-executable",
            description="Windows Portable Executable (PE / DLL / EXE)",
            magic_bytes=b"MZ",
            offset=0,
        ),
        FileSignature(
            category="EXECUTABLE",
            extension="elf",
            mime_type="application/x-executable",
            description="Linux / Unix Executable and Linkable Format (ELF)",
            magic_bytes=b"\x7fELF",
            offset=0,
        ),
        FileSignature(
            category="EXECUTABLE",
            extension="macho",
            mime_type="application/x-mach-binary",
            description="macOS Mach-O Binary (64-bit)",
            magic_bytes=b"\xfe\xed\xfa\xcf",
            offset=0,
        ),
        FileSignature(
            category="EXECUTABLE",
            extension="macho",
            mime_type="application/x-mach-binary",
            description="macOS Mach-O Binary (Reverse)",
            magic_bytes=b"\xcf\xfa\xed\xfe",
            offset=0,
        ),
        # Archives & Compression
        FileSignature(
            category="ARCHIVE",
            extension="zip",
            mime_type="application/zip",
            description="ZIP Archive / OpenXML (DOCX, XLSX, PPTX, APK, JAR)",
            magic_bytes=b"PK\x03\x04",
            offset=0,
        ),
        FileSignature(
            category="ARCHIVE",
            extension="gzip",
            mime_type="application/gzip",
            description="GZIP Compressed Data",
            magic_bytes=b"\x1f\x8b\x08",
            offset=0,
        ),
        FileSignature(
            category="ARCHIVE",
            extension="7z",
            mime_type="application/x-7z-compressed",
            description="7-Zip Archive",
            magic_bytes=b"7z\xbc\xaf\x27\x1c",
            offset=0,
        ),
        FileSignature(
            category="ARCHIVE",
            extension="tar",
            mime_type="application/x-tar",
            description="TAR Tape Archive",
            magic_bytes=b"ustar",
            offset=257,
        ),
        FileSignature(
            category="COMPRESSION",
            extension="zlib",
            mime_type="application/zlib",
            description="ZLIB / Deflate Stream (Default/Best Compression)",
            magic_bytes=b"\x78\x9c",
            offset=0,
        ),
        FileSignature(
            category="COMPRESSION",
            extension="zlib",
            mime_type="application/zlib",
            description="ZLIB / Deflate Stream (Fast/Low Compression)",
            magic_bytes=b"\x78\x01",
            offset=0,
        ),
        FileSignature(
            category="COMPRESSION",
            extension="zlib",
            mime_type="application/zlib",
            description="ZLIB / Deflate Stream (Maximum Compression)",
            magic_bytes=b"\x78\xda",
            offset=0,
        ),
        # Documents
        FileSignature(
            category="DOCUMENT",
            extension="pdf",
            mime_type="application/pdf",
            description="Adobe Portable Document Format (PDF)",
            magic_bytes=b"%PDF-",
            offset=0,
        ),
        # Images
        FileSignature(
            category="IMAGE",
            extension="png",
            mime_type="image/png",
            description="Portable Network Graphics (PNG)",
            magic_bytes=b"\x89PNG\r\n\x1a\n",
            offset=0,
        ),
        FileSignature(
            category="IMAGE",
            extension="jpg",
            mime_type="image/jpeg",
            description="JPEG Image",
            magic_bytes=b"\xff\xd8\xff",
            offset=0,
        ),
        FileSignature(
            category="IMAGE",
            extension="gif",
            mime_type="image/gif",
            description="GIF Image (89a / 87a)",
            magic_bytes=b"GIF8",
            offset=0,
        ),
        # Web Exploitation & Deserialization Magic Signatures
        FileSignature(
            category="SERIALIZATION",
            extension="java-ser",
            mime_type="application/x-java-serialized-object",
            description="Java Serialized Object (ysoserial / RCE gadget chain)",
            magic_bytes=b"\xac\xed\x00\x05",
            offset=0,
        ),
        FileSignature(
            category="SERIALIZATION",
            extension="viewstate",
            mime_type="application/x-aspnet-viewstate",
            description="ASP.NET ViewState Serialized Object",
            magic_bytes=b"\xff\x01",
            offset=0,
        ),
        FileSignature(
            category="SERIALIZATION",
            extension="pickle",
            mime_type="application/x-python-pickle",
            description="Python Pickle Serialized Stream (Remote Code Execution)",
            magic_bytes=b"\x80\x04",
            offset=0,
        ),
        FileSignature(
            category="SERIALIZATION",
            extension="pickle",
            mime_type="application/x-python-pickle",
            description="Python Pickle Stream (Protocol 3)",
            magic_bytes=b"\x80\x03",
            offset=0,
        ),
        FileSignature(
            category="SECURITY",
            extension="crt",
            mime_type="application/x-x509-ca-cert",
            description="X.509 Certificate ASN.1 DER Stream",
            magic_bytes=b"\x30\x82",
            offset=0,
        ),
        # Shellcode / Raw
        FileSignature(
            category="SHELLCODE",
            extension="bin",
            mime_type="application/octet-stream",
            description="x86 / x64 NOP Sled Sequence (Shellcode Stager)",
            magic_bytes=b"\x90\x90\x90\x90",
            offset=0,
        ),
    ]

    @classmethod
    def identify(cls, data: bytes) -> Optional[FileSignature]:
        """
        Inspects the magic bytes of raw data against the signature catalog.
        """
        if not data:
            return None
        
        for sig in cls.SIGNATURES:
            end_offset = sig.offset + len(sig.magic_bytes)
            if len(data) >= end_offset:
                if data[sig.offset:end_offset] == sig.magic_bytes:
                    return sig
                    
        return None

    @classmethod
    def is_powershell_utf16le(cls, data: bytes) -> Tuple[bool, Optional[str]]:
        """
        Detects if raw bytes represent a UTF-16LE encoded PowerShell script.
        PowerShell's -EncodedCommand encodes UTF-16LE bytes, which feature
        alternating null bytes for standard ASCII characters.
        """
        if len(data) < 4 or len(data) % 2 != 0:
            return False, None
        
        try:
            decoded = data.decode("utf-16le")
            # Look for common PowerShell indicators
            indicators = [
                "iex", "invoke-expression", "downloadstring", "new-object",
                "net.webclient", "bypass", "get-process", "powershell",
                "cmd.exe", "whoami", "$env:", "start-process", "system.net"
            ]
            lower = decoded.lower()
            if any(token in lower for token in indicators) or all(32 <= ord(c) < 127 or c in "\r\n\t" for c in decoded):
                return True, decoded
        except UnicodeDecodeError:
            pass
            
        return False, None

    @classmethod
    def is_text(cls, data: bytes) -> Tuple[bool, Optional[str]]:
        """Checks if the data is valid UTF-8 / ASCII text."""
        try:
            text = data.decode("utf-8")
            # Count printable characters
            printable = sum(1 for ch in text if ch.isprintable() or ch in "\r\n\t")
            if len(text) > 0 and (printable / len(text)) > 0.90:
                return True, text
        except UnicodeDecodeError:
            pass
        return False, None
