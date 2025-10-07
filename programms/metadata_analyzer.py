# -----------------------------------------------------------------------------
# Copyright (c) 2025 pxwild. All Rights Reserved.
# pxwild PROPRIETARY AND CONFIDENTIAL — NOT FOR MODIFICATION OR REDISTRIBUTION.
#
# This software and its source code are proprietary to pxwild. Unauthorized
# copying, modification, distribution, decompilation, reverse engineering, or
# creation of derivative works is strictly prohibited without prior written
# permission from pxwild. Any attempt to modify or remove this notice is a
# material breach of the license and will be acted upon to the fullest extent
# permitted by law.
# -----------------------------------------------------------------------------

import os
import argparse
import json
from datetime import datetime
import hashlib
import mimetypes

def analyze_metadata(file_path):
    print(f"\n[*] Metadata Analysis for: {file_path}")
    print("[*] Extracting comprehensive file metadata...\n")
    
    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}")
        return None
    
    metadata = {
        "file_path": file_path,
        "timestamp": datetime.now().isoformat(),
        "basic_info": {},
        "file_hashes": {},
        "permissions": {},
        "timestamps": {},
        "analysis": {}
    }
    
    print("[*] Basic File Information:")
    try:
        stat = os.stat(file_path)
        
        metadata["basic_info"] = {
            "filename": os.path.basename(file_path),
            "directory": os.path.dirname(file_path),
            "size_bytes": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "file_extension": os.path.splitext(file_path)[1],
            "mime_type": mimetypes.guess_type(file_path)[0] or "Unknown"
        }
        
        print(f"    Filename: {metadata['basic_info']['filename']}")
        print(f"    Size: {metadata['basic_info']['size_mb']} MB")
        print(f"    Extension: {metadata['basic_info']['file_extension']}")
        print(f"    MIME Type: {metadata['basic_info']['mime_type']}")
        
    except Exception as e:
        metadata["basic_info"]["error"] = str(e)
        print(f"    Error: {str(e)}")
    
    # File hashes
    print(f"\n[*] File Hashes:")
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            
        metadata["file_hashes"] = {
            "md5": hashlib.md5(content).hexdigest(),
            "sha1": hashlib.sha1(content).hexdigest(),
            "sha256": hashlib.sha256(content).hexdigest()
        }
        
        print(f"    MD5: {metadata['file_hashes']['md5']}")
        print(f"    SHA1: {metadata['file_hashes']['sha1']}")
        print(f"    SHA256: {metadata['file_hashes']['sha256']}")
        
    except Exception as e:
        metadata["file_hashes"]["error"] = str(e)
        print(f"    Error: {str(e)}")
    
    print(f"\n[*] File Permissions:")
    try:
        stat = os.stat(file_path)
        metadata["permissions"] = {
            "mode": oct(stat.st_mode),
            "readable": os.access(file_path, os.R_OK),
            "writable": os.access(file_path, os.W_OK),
            "executable": os.access(file_path, os.X_OK)
        }
        
        print(f"    Mode: {metadata['permissions']['mode']}")
        print(f"    Readable: {metadata['permissions']['readable']}")
        print(f"    Writable: {metadata['permissions']['writable']}")
        print(f"    Executable: {metadata['permissions']['executable']}")
        
    except Exception as e:
        metadata["permissions"]["error"] = str(e)
        print(f"    Error: {str(e)}")
    
    print(f"\n[*] File Timestamps:")
    try:
        stat = os.stat(file_path)
        metadata["timestamps"] = {
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "accessed": datetime.fromtimestamp(stat.st_atime).isoformat()
        }
        
        print(f"    Created: {metadata['timestamps']['created']}")
        print(f"    Modified: {metadata['timestamps']['modified']}")
        print(f"    Accessed: {metadata['timestamps']['accessed']}")
        
    except Exception as e:
        metadata["timestamps"]["error"] = str(e)
        print(f"    Error: {str(e)}")
    
    if metadata["basic_info"].get("file_extension", "").lower() in ['.jpg', '.jpeg', '.png', '.tiff', '.gif']:
        print(f"\n[*] Image Metadata:")
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            
            with Image.open(file_path) as img:
                exif_data = {}
                if hasattr(img, '_getexif'):
                    exif = img._getexif()
                    if exif is not None:
                        for tag_id, value in exif.items():
                            tag = TAGS.get(tag_id, tag_id)
                            exif_data[tag] = value
                
                metadata["image_metadata"] = {
                    "dimensions": img.size,
                    "format": img.format,
                    "mode": img.mode,
                    "exif_data": exif_data
                }
                
                print(f"    Dimensions: {img.size}")
                print(f"    Format: {img.format}")
                print(f"    Mode: {img.mode}")
                print(f"    EXIF Tags: {len(exif_data)}")
                
        except ImportError:
            metadata["image_metadata"] = {"error": "PIL not installed"}
            print("    Error: PIL library not installed")
        except Exception as e:
            metadata["image_metadata"] = {"error": str(e)}
            print(f"    Error: {str(e)}")
    
    metadata["analysis"] = {
        "file_type": "image" if metadata["basic_info"].get("file_extension", "").lower() in ['.jpg', '.jpeg', '.png', '.tiff', '.gif'] else "other",
        "has_exif": "image_metadata" in metadata and "exif_data" in metadata.get("image_metadata", {}),
        "analysis_complete": True
    }
    
    filename = f"metadata_analysis_{os.path.basename(file_path)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\n[*] Analysis saved to: {filename}")
    print(f"[*] File type: {metadata['analysis']['file_type']}")
    print(f"[*] Has EXIF data: {metadata['analysis']['has_exif']}")
    
    return metadata

def main():
    parser = argparse.ArgumentParser(description="Metadata Analyzer")
    parser.add_argument("--target", help="File path to analyze", required=False)
    args = parser.parse_args()
    
    file_path = args.target if args.target else input("\n[?] Enter file path to analyze: ").strip()
    
    if not file_path:
        print("[!] No file path provided!")
        return
    
    analyze_metadata(file_path)

if __name__ == "__main__":
    main()

