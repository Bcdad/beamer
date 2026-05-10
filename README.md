# Beamer PDF to PowerPoint 转换工具

将 LaTeX Beamer 生成的 PDF 演示文稿一键转换为 PPTX 格式。

## 安装依赖

```bash
pip install pdf2pptx
```

具体版本如下

```
conda list pdf2ppt
# packages in environment at C:\Users\86139\anaconda3\envs\pdf2ppt:
#
# Name                    Version                   Build  Channel
pdf2pptx                  1.0.5                    pypi_0    pypi
```

## 使用方法

### 转换单个文件

```bash
# 最简单的用法：自动输出同名 .pptx 文件
python beamer2pptx.py presentation.pdf

# 指定输出文件名
python beamer2pptx.py presentation.pdf -o output.pptx

# 调整分辨率（默认 300 DPI）
python beamer2pptx.py presentation.pdf --dpi 150
```

### 批量转换

```bash
# 转换目录下所有 PDF 文件
python beamer2pptx.py --batch ./slides/

# 批量转换并指定输出目录
python beamer2pptx.py --batch ./slides/ -o ./pptx_output/
```

### 命令行参数

| 参数 | 说明 |
|------|------|
| `input` | 输入的 PDF 文件路径（或目录，使用 `--batch` 时） |
| `-o, --output` | 输出的 PPTX 文件路径（或目录） |
| `--dpi` | 图像分辨率，默认 300 |
| `--batch` | 批量模式：转换目录下所有 PDF 文件 |

## 示例

```bash
# 转换毕业设计演示文稿
cd d:\study\毕业设计\src
python tools/beamer2pptx.py docs/毕设一.pdf

# 批量转换 docs 目录下的所有 PDF
python tools/beamer2pptx.py --batch docs/ -o PPT/
```

## 注意事项

1. **转换原理**：该工具将 PDF 的每一页转换为高分辨率图片，然后嵌入到 PPTX 幻灯片中
2. **编辑性**：转换后的 PPT 不可直接编辑文字，如需修改请回到 LaTeX 源文件
3. **文件大小**：高 DPI 会增加输出文件大小，如需减小可降低 DPI（如 150）
4. **动画效果**：Beamer 的动画效果会被转换为静态图片，无法在 PPT 中播放

## 常见问题

**Q: 转换后文字模糊怎么办？**
A: 增加 DPI 值，如 `--dpi 400`

**Q: 输出文件太大怎么办？**
A: 降低 DPI 值，如 `--dpi 150`

**Q: 支持其他 PDF 格式吗？**
A: 支持任何 PDF 文件，不仅限于 Beamer 生成的
