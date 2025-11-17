"""
XML 座標轉換工具

將 XML 檔案中的 X_COORD 和 Y_COORD 進行座標轉換（X = -X + 25, Y = -Y + 25），
並相應地修改檔名中的座標值。
"""

import re
from pathlib import Path
from typing import Tuple


def transform_coordinate(value: int) -> int:
    """
    轉換座標值。
    
    Args:
        value: 原始座標值
        
    Returns:
        轉換後的座標值 (-value + 25)
    """
    return -value + 25


def transform_xml_content(content: str) -> str:
    """
    轉換 XML 檔案內容中的座標值。
    
    Args:
        content: 原始 XML 內容
        
    Returns:
        轉換後的 XML 內容
    """
    def replace_x_coord(match):
        value = int(match.group(1))
        new_value = transform_coordinate(value)
        return f"<X_COORD>{new_value}</X_COORD>"
    
    def replace_y_coord(match):
        value = int(match.group(1))
        new_value = transform_coordinate(value)
        return f"<Y_COORD>{new_value}</Y_COORD>"
    
    # 替換 X_COORD
    content = re.sub(r'<X_COORD>(-?\d+)</X_COORD>', replace_x_coord, content)
    # 替換 Y_COORD
    content = re.sub(r'<Y_COORD>(-?\d+)</Y_COORD>', replace_y_coord, content)
    
    return content


def transform_filename(filename: str) -> str:
    """
    轉換檔名中的座標值。
    
    例如：1830002926_A2LPAC14A1-FAKY25420001-0-0_SM1C10011 25-023-010.xml
    轉換為：1830002926_A2LPAC14A1-FAKY25420001-0-0_SM1C10011 25-002-015.xml
    
    Args:
        filename: 原始檔名
        
    Returns:
        轉換後的檔名
    """
    # 匹配檔名模式：最後兩組被 '-' 分隔的數字
    pattern = r'(-\d+)(-\d+)(\.xml)$'
    match = re.search(pattern, filename)
    
    if match:
        x_str = match.group(1)  # 例如：-023
        y_str = match.group(2)  # 例如：-010
        extension = match.group(3)  # .xml
        
        # 提取數字部分（去掉前面的 '-'）
        x_value = int(x_str[1:])  # 023
        y_value = int(y_str[1:])  # 010
        
        # 進行座標轉換
        new_x = transform_coordinate(x_value)
        new_y = transform_coordinate(y_value)
        
        # 重建檔名
        base_name = filename[:match.start()]
        new_filename = f"{base_name}-{new_x:03d}-{new_y:03d}{extension}"
        
        return new_filename
    
    return filename


def process_xml_files(input_dir: str, output_dir: str) -> None:
    """
    處理指定資料夾中的所有 XML 檔案。
    
    Args:
        input_dir: 輸入資料夾路徑
        output_dir: 輸出資料夾路徑
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # 建立輸出資料夾
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 取得所有 XML 檔案
    xml_files = list(input_path.glob("*.xml"))
    
    if not xml_files:
        print(f"在 {input_dir} 中找不到 XML 檔案。")
        return
    
    print(f"找到 {len(xml_files)} 個 XML 檔案，開始處理...")
    
    for xml_file in xml_files:
        try:
            # 讀取 XML 內容
            content = xml_file.read_text(encoding='utf-8')
            
            # 轉換 XML 內容
            new_content = transform_xml_content(content)
            
            # 轉換檔名
            new_filename = transform_filename(xml_file.name)
            
            # 寫入新檔案
            output_file = output_path / new_filename
            output_file.write_text(new_content, encoding='utf-8')
            
            print(f"✓ {xml_file.name} → {new_filename}")
            
        except Exception as e:
            print(f"✗ 處理 {xml_file.name} 時發生錯誤：{e}")
    
    print(f"\n處理完成！檔案已儲存至：{output_dir}")


if __name__ == "__main__":
    # 設定輸入和輸出資料夾
    INPUT_DIR = r"C:\KGD\Data\SM1C10011 25"
    OUTPUT_DIR = r"C:\KGD\Data\SM1C10011 25_New"
    
    process_xml_files(INPUT_DIR, OUTPUT_DIR)

