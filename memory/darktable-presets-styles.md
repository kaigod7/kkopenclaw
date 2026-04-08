# Darktable 优质预设 & 风格参数大全

> 学习来源：pixls.us 社区、darktable 官方文档、t3mujinpack GitHub、dpreview 等
> 生成时间：2026-04-08

---

## 📌 快速工作流（通用起点）

**基础流程（所有类型通用）：**
```
1. 校准（Color Calibration）→ 2. 曝光（Exposure）→ 3. 镜头校正
4. 去噪（Denoise profiled）→ 5. Filmic RGB → 6. TonemapEQ / Sigmoid
7. 锐化（Diffuse or Sharpen）→ 8. Color Balance RGB
```

**modern 设置（darktable 4.2+）：**
- `settings > processing > auto apply pixel workflow defaults`: scene-referred (filmic)
- `auto apply per chromatic adaptation defaults`: modern

---

## 🏞️ 风景照（Landscape）

### 基础参数
| 模块 | 参数 | 说明 |
|------|------|------|
| Filmic RGB | grey exposure → 0 | 中间灰基准 |
| Filmic RGB | contrast → 1.0-1.5 | 对比度 |
| Filmic RGB | white relative exposure → -2.5 | 白点 |
| Filmic RGB | black relative exposure → +4.0 | 暗部提亮 |
| Tone Equalizer | highlights → -0.3 | 压高光 |
| Tone Equalizer | shadows → +0.2 | 提阴影 |
| Color Balance RGB | saturation → +10-20 | 轻微饱和 |
| Diffuse or Sharpen | preset: lens deblur medium | 镜头去模糊 |

### 经典风格（DtStyle）
- **Velviatic**：仿富士 Velvia，高饱和·高对比，适合花卉/建筑/风景
- **Sunset Bliss**：蓝橙日落色调，风景夕阳专用
- **Pastel**：仿富士 Provia，柔和百搭

### HSV 调色
```python
# OpenCV 风景调色（BGR 转 HSV 调饱和度亮度）
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsv[:,:,1] *= 1.5   # 饱和度×1.5
hsv[:,:,2] *= 1.2   # 亮度×1.2
result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
```

---

## 👤 人像 / 人物（Portrait）

### Skin Tone Editor（darktable 新模块！）
- 不是简单降饱和，而是把偏色像素「转移」到目标健康肤色
- 工作在 Jz 色彩空间，保持阴影/高光体积感
- 用滴管在面部健康肤色区域取样

### Channel Mixer 黑白人像
```python
# 平滑皮肤（减少纹理）
R=0.9, G=0.3, B=-0.3

# 增强细节
R=0.4, G=0.75, B=-0.15
```

### Teal / Orange 电影感人像
**两实例 Color Balance RGB + 蒙版：**
- 实例1：排除皮肤，背景→青蓝色（Shadows → 蓝/青）
- 实例2：仅皮肤，暖橙色调（Highlights → 橙/红）

### 人像精修参数
| 模块 | 参数 |
|------|------|
| Color Calibration | CAT:适应→稳定，主体肤色段 |
| Color Balance RGB | saturation → -10（降饱和更柔和） |
| Color Balance RGB | brilliance → +5-15（中间调提亮） |
| Shadows → -10 | 让皮肤更有立体感 |
| Highlights → +5 | 恢复高光细节 |

---

## 🐾 宠物 / 动物（Pet & Wildlife）

### 宠物摄影核心原则
- **白色宠物**：降低高光恢复毛发细节，避免过曝成白色块
- **黑色宠物**：防止过曝
- **金色/棕色毛发**：暖色调处理
- **银灰毛发**：蓝色调处理

### Darktable 野生动物蒙版锐化
```
1. Diffuse or Sharpen → "lens deblur | medium" 预设
2. 用亮度蒙版只锐化主体（动物），不动背景
3. 背景虚化 = 反向蒙版（用另一个实例模糊背景）
```

### 白平衡关键
- 白/奶白色毛发最容易受环境色偏影响
- Auto WB 对白色毛发容易误判，建议手动校准

---

## 🏙️ 人文 / 街拍（Street & Documentary）

### 城市人文经典工作流
**Color Balance RGB 是核心模块！**

**Teal/Orange 色调（青橙分离）：**
```
Color Balance RGB → 全局饱和度降至 30-40
Shadows → 蓝/青色（-20 到 -40）
Highlights → 橙/暖色（+10 到 +20）
```

**暗调电影感：**
- Filmic RGB → grey exposure 偏暗
- Black relative → +3.5
- Color Balance RGB → 全局对比 +10

### 快速简单预设（pixls.us 社区）
**必装模块：**
- Filmic RGB, Color Balance RGB, Diffuse or sharpen
- Color Calibration, Crop, Tone Equalizer, Exposure
- Denoise (profiled), Highlight Reconstruction

**参数调整顺序：**
```
1. Color Assessment Mode（Ctrl+B）
2. Exposure → 设中间灰点
3. Filmic RGB → 设白点黑点
4. Sigmoid（现代替代 filmic）→ 对比度
5. Color Balance RGB → 色调
```

---

## 🎬 电影感（ Cine / Cinematic）

### 核心三要素
1. **压高光 + 提阴影**（扩大动态范围感）
2. **青/橙色调分离**（Color Balance RGB 两实例）
3. **轻度去饱和**（saturation → 80-90）

### 色调分离参数
```python
# Shadows 实例：蓝色/青色偏移
# Highlights 实例：橙色/红色偏移
# Midtones 保持中性或微暖
```

### LUT 3D 模块
- darktable 内置 Velvia 预设
- 可加载第三方 LUT 做胶片模拟
- **推荐资源：**
  - t3mujinpack（GitHub，免费）
  - 官方 LUT 库

---

## 📷 胶片模拟（Film Emulation）

### 最全免费预设包：t3mujinpack
GitHub: `github.com/t3mujinpack/t3mujinpack`

**黑白胶片：**
| 型号 | 风格 |
|------|------|
| Ilford HP5 Plus 400 | 经典黑白，人文首选 |
| Ilford Tri-X 400 | 高对比粗颗粒 |
| Ilford Delta 400 | 细腻灰度过渡 |
| Kodak Tri-X 400 | 经典美式黑白 |
| Kodak T-Max 3200 | 极高感黑白 |

**彩色负片：**
| 型号 | 风格 |
|------|------|
| Kodak Portra 400 | 人像神片，柔和自然 |
| Kodak Portra 800 | 弱光/黄昏 |
| Kodak Gold 200 | 暖调高饱和 |
| Kodak Ektar 100 | 极高饱和+细颗粒 |
| Fuji Pro 400H | 柔和低对比 |
| Fuji Superia 400 | 日系家庭感 |

**彩色反转片：**
| 型号 | 风格 |
|------|------|
| Fuji Velvia 50 | 风景王者，高饱和 |
| Fuji Provia | 自然柔和 |
| Fuji Astia | 人像专用，柔美 |

### 富士胶片模拟（darktable 专用预设）
- **Classic Chrome**：低饱和+强对比，纪实感
- **Pro Neg Hi/Std**：专业负片风格
- **Eterna Cinema**：电影感低饱和
- **Acros**：黑白质感（可加红滤镜）

---

## 🎨 艺术风格 / 创意效果

### 怀旧/复古（Vintage）
**参数组合：**
```
Filmic RGB → 低对比 + 高黑色
Color Zones → 暖化中间调
Tone Curve → S 形轻微压暗
饱和度 → -15
```

### 黑白艺术（Artistic B&W）
```python
# Channel Mixer Gray Tab 人像优化
R=0.8, G=0.3, B=-0.2  # 光滑皮肤
R=0.5, G=0.6, B=-0.2  # 一般用途
```

### DALLE/风格转换思路
```
原始图 → CLIP Interrogator → 分析风格
风格参考图 → 颜色直方图匹配
```

---

## 🖼️ 二次元 / 动漫风格

### Python 动漫图片处理

**线稿提取（OpenCV）：**
```python
import cv2

# 提取线稿用于上色任务
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
dilated = cv2.dilate(gray, kernel, iterations=1)
line = cv2.divide(gray, dilated, scale=255)
```

**动漫上色模型（Pix2Pix cGAN）：**
- 输入：黑白线稿
- 输出：彩色动漫图
- 训练数据：Danbooru 动漫数据集（需自己处理）

**Waifu2x（图片放大）：**
```bash
# 降噪 + 2倍放大（动漫首选）
waifu2x-converter -m noise_scale -n 2 -i input.png -o output.png

# 纯降噪
waifu2x-converter -m noise -n 2 -i input.png -o output.png
```

**AnimeGANv2（照片转动漫风）：**
```python
# 需要 TensorFlow
# 输入真实照片 → 输出动漫风格
```

**Color Hints 引导上色：**
- 在图上指定颜色点作为引导
- 用于指定特定部位的颜色（如头发、服装）

### 二次元风格调色（Python + OpenCV）
```python
# 动漫风：提高饱和度，稍微压暗
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsv[:,:,1] *= 1.4   # 饱和度提高
hsv[:,:,2] = np.clip(hsv[:,:,2] * 0.9, 0, 255)  # 轻微压暗
anime = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# 边缘增强（让线条更清晰）
anime = cv2.edgePreservingFilter(anime, flags=1, sigma_s=60, sigma_r=0.4)
```

### AI 在线动漫上色
- **Artificial Studio**：上传线稿，AI 自动上色
- **Style Customization**：输入文字描述风格（吉卜力/王道热血等）

---

## 🔧 Python 修图效率工具

### 批量预设应用
```python
import subprocess
import os

# 用 darktable-cli 批量导出
for f in os.listdir(input_dir):
    cmd = [
        'darktable-cli',
        os.path.join(input_dir, f),
        os.path.join(output_dir, f),
        '--style', 'portra_400',  # 应用预设
        '--core', '--conf', 'plugins/lighttable/lowquel=0'
    ]
    subprocess.run(cmd)
```

### OpenCV 基础操作
```python
import cv2

# 读取（OpenCV 是 BGR！）
img = cv2.imread('input.jpg')

# 缩放
resized = cv2.resize(img, (1920, 1080))

# 裁剪
cropped = img[y:y+h, x:x+w]

# 旋转
(h, w) = img.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated = cv2.warpAffine(img, M, (w, h))
```

### scikit-image 高级用法
```python
from skimage import filters, segmentation, morphology

# 自动阈值分割（Otsu）
threshold = filters.threshold_otsu(gray_img)
binary = gray_img > threshold

# 超像素分割（类似 SLIC）
segments = segmentation.slic(img, n_segments=200)

# 形态学去噪声
opened = morphology.opening(img, footprint=morphology.disk(3))
closed = morphology.closing(img, footprint=morphology.disk(3))
```

### rembg 批量去背
```python
from rembg import remove, new_session
from PIL import Image
import os

session = new_session("birefnet-general")

for f in os.listdir('photos'):
    img = Image.open(f'photos/{f}')
    output = remove(img, session=session, alpha_matting=True)
    output.save(f'output/{f}')
```

---

## 📋 模块速查表

| 场景 | 推荐模块 |
|------|----------|
| 基础曝光 | Exposure |
| RAW 校准 | Color Calibration |
| 高级调色 | Color Balance RGB |
| 风景对比 | Filmic RGB + Tone Equalizer |
| 人像肤色 | Skin Tone Editor + Color Balance RGB |
| 蒙版锐化 | Diffuse or Sharpen |
| 风格/ LUT | LUT 3D + Velvia |
| 局部调整 | Color Zones + Parametric Mask |
| 黑白转换 | Channel Mixer (gray tab) |
| 去背景 | rembg (Python) |
| 批量处理 | darktable-cli (bash) |

---

## 🌐 推荐资源

- **t3mujinpack**（GitHub）：最全免费胶片模拟预设
- **pixls.us 社区**：darktable 用户最大社区
- **darktable 官方手册**：docs.darktable.org
- **darktable-chart**：从色彩卡自动生成风格
- **Waifu2x**：动漫图片超分辨率
- **AnimeGANv2**：照片转动漫风

---

*最后更新：2026-04-08*
