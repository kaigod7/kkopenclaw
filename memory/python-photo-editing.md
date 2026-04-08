# Python 修图技巧笔记

## 库的选择

| 库 | 用途 | 难度 |
|---|---|---|
| Pillow | 基础操作：裁剪、缩放、旋转、调色 | ⭐ 最简单 |
| OpenCV | 高级调色、人脸检测、批处理 | ⭐⭐ 中等 |
| scikit-image | 科学图像分析、分割、滤波 | ⭐⭐ 中等 |
| rembg | AI 去背景 | ⭐ 最简单 |
| Wand | ImageMagick 绑定，格式转换、特效 | ⭐⭐ 中等 |
| Matplotlib | 可视化、绘图 | ⭐ 简单 |

## Pillow 基础

```python
from PIL import Image, ImageEnhance, ImageFilter

img = Image.open("input.jpg")

# 缩放、旋转、翻转
img.resize((800, 600))
img.rotate(45)
img.transpose(Image.FLIP_LEFT_RIGHT)

# 调色
ImageEnhance.Contrast(img).enhance(1.5)   # 对比度
ImageEnhance.Color(img).enhance(1.3)        # 饱和度
ImageEnhance.Sharpness(img).enhance(1.2)   # 锐度
ImageEnhance.Brightness(img).enhance(1.1)  # 亮度

# 滤镜
img.filter(ImageFilter.GaussianBlur(radius=2))
img.filter(ImageFilter.EDGE_ENHANCE)

# 腐蚀/膨胀（去噪声）
for _ in range(3):
    img = img.filter(ImageFilter.MinFilter(3))  # 腐蚀
```

## OpenCV 调色

**⚠️ 注意：OpenCV 读图是 BGR，不是 RGB！混用时要转换。**

```python
import cv2
import numpy as np

img = cv2.imread("input.jpg")
bgr = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # 转 RGB 给 Pillow/Matplotlib
rgb = cv2.cvtColor(bgr, cv2.COLOR_RGB2BGR)   # 转回来给 OpenCV

# HSV 调色（最常用的修图方法）
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsv[:,:,1] *= 1.5   # 饱和度 ×1.5
hsv[:,:,2] *= 1.2   # 亮度 ×1.2
result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# 自动白平衡（LAB 色彩空间 + CLAHE）
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
l, a, b = cv2.split(lab)
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
l = clahe.apply(l)
result = cv2.cvtColor(cv2.merge((l,a,b)), cv2.COLOR_LAB2BGR)

# 直方图匹配（模仿另一张图的色调）
matched = cv2.match_histograms(img, ref_img, channel=2)

# 边缘检测
edges = cv2.Canny(img, 100, 200)

# 双边滤波（保边模糊，比 Gaussian 更好）
blur = cv2.bilateralFilter(img, 15, 75, 75)

# 图像融合
blended = cv2.addWeighted(img1, 0.7, img2, 0.3, 0)

# 批量灰度处理
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

## scikit-image

```python
from skimage import io, filters, morphology, segmentation, restoration

# 边缘检测
edges = filters.sobel(gray)

# 去噪（非局部均值，比双边滤波更好）
denoised = restoration.denoise_nl_means(img, h=0.1)

# Otsu 自动阈值分割
threshold = filters.threshold_otsu(gray)
binary = gray > threshold

# 形态学：去小白点 / 填小黑点
opened = morphology.opening(img, footprint=morphology.disk(3))
closed = morphology.closing(img, footprint=morphology.disk(3))

# Skeletonize 细化
skel = morphology.skeletonize(img > threshold)

# SLIC 超像素分割
segments = segmentation.slic(img, n_segments=200)

# Random Walker 分割（需要预标标记）
labels = segmentation.random_walker(gray, markers)
```

## rembg（AI 去背景）

```python
from rembg import remove, new_session
from PIL import Image
import os

# 基础用法
output = remove(Image.open("input.jpg"))
output.save("output.png")  # 必须 PNG，支持透明通道！

# Alpha Matting（发丝等细节更干净）
output = remove(img, alpha_matting=True)

# 换背景颜色
gray_bg = Image.new("RGBA", output.size, (200, 200, 200, 255))
final = Image.alpha_composite(gray_bg, output)
final.convert("RGB").save("gray_bg.jpg")

# 批量处理（用 session 提速）
session = new_session("birefnet-general")
for f in os.listdir("input/"):
    out = remove(Image.open(f"input/{f}"), session=session)
    out.save(f"output/{f}")

# 注意：图片太大会 OOM，先 resize
```

## Wand（ImageMagick 绑定）

```python
from wand.image import Image as WandImage

with WandImage(filename="input.jpg") as img:
    img.resize(800, 600)
    img.rotate(45)
    img.flip()
    img.effect_sharpen(radius=1, sigma=1)
    img.save(filename="output.jpg")
```

## 实战：完整修图流程

```python
# 1. 打开图片
from PIL import Image
import cv2
import numpy as np

img = Image.open("photo.jpg")

# 2. 基础调整（用 Pillow）
from PIL import ImageEnhance
img = ImageEnhance.Contrast(img).enhance(1.3)
img = ImageEnhance.Color(img).enhance(1.2)

# 3. 转 OpenCV 做高级调色
arr = np.array(img)
bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
hsv[:,:,1] *= 1.2
hsv[:,:,2] *= 1.1
enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# 4. 用 rembg 去背景
from rembg import remove
result = remove(Image.fromarray(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)))
result.save("edited.png")
```

## 注意事项

- **OpenCV 是 BGR**，Pillow/Matplotlib 是 RGB，混用记得转
- **rembg 必须存 PNG**，JPG 不支持透明通道
- **图片太大先 resize**，否则会 OOM
- **批量处理用 session**，避免重复加载模型
- **修图顺序**：裁剪 → 基础曝光/白平衡 → 降噪 → 对比度/饱和度 → 锐化 → 输出
