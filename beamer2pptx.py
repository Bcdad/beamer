#!/usr/bin/env python3
"""
Beamer PDF to PowerPoint 转换工具
将 LaTeX Beamer 生成的 PDF 演示文稿转换为 PPTX 格式
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from pdf2pptx import convert_pdf2pptx
except ImportError:
    print("错误: 缺少必要的依赖库。")
    print("请先运行: pip install pdf2pptx")
    sys.exit(1)


def convert_beamer_to_pptx(pdf_path: str, output_path: str = None, dpi: int = 300) -> str:
    """
    将 Beamer PDF 转换为 PPTX 文件

    Args:
        pdf_path: 输入的 PDF 文件路径
        output_path: 输出的 PPTX 文件路径（可选，默认与 PDF 同名）
        dpi: 图像分辨率，默认 300 DPI

    Returns:
        生成的 PPTX 文件路径
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF 文件不存在: {pdf_path}")

    if not pdf_path.suffix.lower() == '.pdf':
        raise ValueError(f"输入文件必须是 PDF 格式，当前格式: {pdf_path.suffix}")

    # 生成输出路径
    if output_path is None:
        output_path = pdf_path.with_suffix('.pptx')
    else:
        output_path = Path(output_path)

    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"正在转换: {pdf_path.name} -> {output_path.name}")
    print(f"分辨率: {dpi} DPI")

    try:
        # 转换所有页面 (page_count=None 表示全部)
        convert_pdf2pptx(str(pdf_path), str(output_path), resolution=dpi, start_page=0, page_count=None)
        print(f"转换成功: {output_path}")
        return str(output_path)
    except Exception as e:
        print(f"转换失败: {e}")
        sys.exit(1)


def batch_convert(input_dir: str, output_dir: str = None, dpi: int = 300):
    """
    批量转换目录下所有 PDF 文件

    Args:
        input_dir: 输入目录
        output_dir: 输出目录（可选，默认在输入目录下创建 pptx_output 子目录）
        dpi: 图像分辨率
    """
    input_dir = Path(input_dir)

    if not input_dir.is_dir():
        print(f"错误: 目录不存在: {input_dir}")
        sys.exit(1)

    if output_dir is None:
        output_dir = input_dir / "pptx_output"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = list(input_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"未找到 PDF 文件: {input_dir}")
        return

    print(f"找到 {len(pdf_files)} 个 PDF 文件")
    print(f"输出目录: {output_dir}\n")

    success_count = 0
    for pdf_file in pdf_files:
        try:
            output_file = output_dir / pdf_file.with_suffix('.pptx').name
            convert_beamer_to_pptx(pdf_file, output_file, dpi)
            success_count += 1
        except Exception as e:
            print(f"跳过 {pdf_file.name}: {e}")

    print(f"\n批量转换完成: {success_count}/{len(pdf_files)} 成功")


def main():
    parser = argparse.ArgumentParser(
        description="Beamer PDF to PowerPoint 转换工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 转换单个文件
  python beamer2pptx.py presentation.pdf

  # 指定输出文件名
  python beamer2pptx.py presentation.pdf -o my_presentation.pptx

  # 批量转换目录下所有 PDF
  python beamer2pptx.py --batch ./slides/

  # 批量转换并指定输出目录
  python beamer2pptx.py --batch ./slides/ -o ./pptx_output/
        """
    )

    parser.add_argument(
        "input",
        help="输入的 PDF 文件路径或目录（使用 --batch 时）"
    )
    parser.add_argument(
        "-o", "--output",
        help="输出的 PPTX 文件路径或目录"
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="图像分辨率（默认 300）"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="批量模式：转换目录下所有 PDF 文件"
    )

    args = parser.parse_args()

    if args.batch:
        batch_convert(args.input, args.output, args.dpi)
    else:
        convert_beamer_to_pptx(args.input, args.output, args.dpi)


if __name__ == "__main__":
    main()
