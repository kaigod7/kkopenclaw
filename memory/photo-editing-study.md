# 修图技术学习笔记（完整版）
## 学习日期：2026-04-09 | 最后更新：2026-04-09（第9轮）

---

## ⚠️ 最新版本速查

| 软件/库 | 最新版本 | 发布日期 |
|---------|----------|----------|
| Lightroom Classic | **15.2** | 2026年2月 |
| Darktable | **5.4.1** | 2026年2月 |
| OpenCV | **4.13.0** | 2025年12月 |
| Pillow | **12.0.0** | 2025年10月 |

---

## 一、Lightroom Classic 15.2 最新功能（2026年2月）

### 🔥 Firefly AI 集成
- **Edit Image**：直接发送照片到 Adobe Firefly，用 prompt 编辑
- **Create Video**：用 AI 把照片转成视频

### 🖼️ WebP 格式支持
- 可以导入、编辑、导出 WebP 文件

### 👥 Assisted Culling 改进
- AI 主体选择和眼部对焦模型升级，更好处理多人合照

---

## 二、Darktable 5.4.x 最新功能

### 🎨 AgX Tone Mapper（新增重点！）
- 基于 Blender's AgX 显示变换，提供丰富的控制选项
- 高光区逐渐去饱和（类似胶片效果）
- **primaries 滑杆**：精调 RGB 主色相
- **preserve hue**：防止色偏

### 📊 示波器升级
- **Waveform / RGB Parade / Vectorscope**

### 🔬 Capture Sharpening（5.4 新增！）
- 内置于 demosaic 模块的锐化功能，专门针对去马赛克后的锐化

---

## 三、Darktable 三大 Tone Mapper 终极对比

| 场景 | 推荐模块 | 原因 |
|------|----------|------|
| 大光比风景 | **Filmic RGB** | 高光保护最好 |
| 日常人像/静物 | **Sigmoid** | 开箱即用 |
| 颜色复杂（花卉/昆虫） | **AgX** | 色相保持最准 |
| 快速批处理 | **Sigmoid** | 调整少出好片 |

### AgX vs Filmic RGB vs Sigmoid
- **Sigmoid**：开箱即用，肤色自然；复杂场景调整空间有限
- **Filmic RGB**：高光重建模式多；日落易偏粉（"三文鱼粉"问题）
- **AgX（5.4 新）**：Sigmoid 简单 + Filmic 控制

### "Notorious 6" 问题
- 高光处各颜色渐变到白色时出现的色偏
- AgX / Sigmoid 可用 preserve hue + 衰减滑杆精确控制

---

## 四、Darktable 降噪模块详解

### 四大降噪模块
| 模块 | 原理 | 适用场景 |
|------|------|----------|
| **RAW Denoise** | RAW 未去马赛前降噪 | 初步降噪（不推荐单独用） |
| **Denoise (Profiled)** | 基于 300+ 相机噪声画像 | 高ISO首选，自动匹配相机 |
| **Denoise (Non-local means)** | 匹配邻域相似像素取均值 | 保留结构，去噪强 |
| **Denoise (Bilateral filter)** | 保边模糊 | 大面积平滑区域 |

### Denoise (Profiled) 核心参数
- **Y0 曲线**：控制亮度噪声（升 = 降噪更强）
- **wavelet vs non-local means**：wavelet 资源消耗更低
- 现在可以**单实例**处理 luma + chroma 噪声（不再需要双实例！）

### 高级降噪技巧
- **双实例法**：第一个实例降色彩噪点；第二个实例专降暗部噪点
- **RAW Denoise**：仅作初步降噪，不要依赖它去除所有噪点（会丢失细节）
- **先降噪，再锐化**：顺序很重要

---

## 五、Darktable 锐化与局部对比度

### Diffuse or Sharpen 模块（最强大！）
核心概念：**扩散**是粒子从高浓度→低浓度的物理过程
- **正向扩散**：模拟模糊、去雾
- **反向扩散**：去模糊、去噪

#### 四阶扩散
| 阶数 | 方向 | 用途 |
|------|------|------|
| 第一阶 | 沿梯度方向 | 基础锐化 |
| 第二阶 | 各向同性扩散 | 平滑 |
| 第三阶 | 沿低频层梯度 | 引导高频扩散方向（保边） |
| 第四阶 | 沿高频层梯度 | **降噪最佳**（保边） |

#### 推荐预设
- **"lens deblur | medium"**：日常锐化
- **"sharpen demosaicing"**：去马赛克后锐化
- **"local contrast | fine"**：局部对比度

### ⚠️ 旧 sharpen 模块已不推荐
- USM 算法在 Lab 色彩空间执行，可能产生不良效果
- 用 **contrast equalizer** 或 **diffuse or sharpen** 代替

### Contrast Equalizer
- 可做 clarity（清晰度）、去模糊、锐化
- 有多个预设可用

---

## 六、Tone Equalizer 模块（高级动态范围压缩）

### 核心原理
- **不是普通曲线**：按亮度区域分别调整曝光，而非逐像素
- 生成**引导蒙版**（edge-aware blur），在保边和区域平滑之间平衡
- 调整蒙版中每个区域内的曝光，同时**保留局部对比度**

### 关键参数
| 参数 | 作用 |
|------|------|
| `luminance estimator` | RGB euclidean norm / RGB sum |
| `preserve details` | no / guided filter（推荐） |
| `exposure/contrast compensation` | 底部核心调整滑杆 |

### Preserve Details 三种模式
- **no**：无平滑，等同于普通曲线，会压缩局部对比度
- **guided filter**（推荐）：保边模糊，但阴影比高光模糊得多（有时是优点！）

### 双实例用法（高级）
1. **第一实例**：压缩高光 → 提亮暗部（compress - expand trick）
2. **第二实例**：对高光做局部对比度增强
3. 两个实例的 mask 类型要分别调，混用会产生光晕

---

## 七、Local Contrast 模块

### 核心算法
- **Local Laplacian（默认）**：对梯度反转和光晕有鲁棒性
- **Bilateral filter**：更快，但效果稍差

### 核心参数
- `bilateral grid`：双边网格模式
- `local laplacian`：
  - **shadow lift**：提亮阴影
  - **highlight compression**：压缩高光
  - **detail boost**：增强细节
  - **modern**：新算法，效果更好

### 与 Tone Equalizer 的区别
- **Local Contrast**：全局调整，在亮度区域内保持细节
- **Tone Equalizer**：分区调整，可以对不同亮度区做不同处理

---

## 八、Darktable 白平衡与色彩校准

### 白平衡模块 vs 色彩校准模块
| 模块 | 性质 | 适用场景 |
|------|------|----------|
| **白平衡（WB）** | 技术性校正 | 基础灰点校正 |
| **色彩校准（CC）** | 感知性适配 | 复杂光源、多光源、肤色 |

### 两种工作流
- **Legacy（传统）**：白平衡模块包揽所有
- **Modern（推荐）**：白平衡做基础 → 色彩校准做感知适配

### CAT 算法
- 色彩校准使用 **Chromatic Adaptation Transformation**
- 可以用**蒙版**做局部白平衡（处理混合光源！）
- **Spot color mapping**：用肤色样本设置白平衡目标值

---

## 九、Darktable Color Balance RGB（高级调色核心）

### 基于 ASC CDL
美国电影摄影师协会色彩决策列表：Slope / Offset / Power

### Master Tab
- 高级饱和度控制：vibrance + chroma + saturation

### 4 Ways Tab（分离色调）
| 参数 | 等同于 | 作用 |
|------|--------|------|
| `global offset` | ASC CDL offset | 加常数RGB值，类似黑场偏移 |
| `shadows lift` | ASC CDL lift | 暗部乘法 |
| `highlights gain` | ASC CDL slope | 高光乘法 |
| `global power` | ASC CDL power | 幂函数 |

### 与 RGB Curves 的本质区别
- **Color Balance RGB**：scene-referred，无界输入输出
- **RGB Curves**：display-referred，有界 0-1 映射
- 4 Ways = lift/gamma/gain/offset 的场景参照版本

### 推荐预设
- **"teal/orange color-grading"**：电影感橙青分离色调（需要两个实例 + 蒙版）

---

## 十、Darktable 修销模块（Retouch）

### 四大工具
| 工具 | 用途 | 原理 |
|------|------|------|
| **Clone（克隆）** | 复制区域覆盖目标 | 直接复制源像素 |
| **Heal（修复）** | 去除瑕疵/污点 | 匹配纹理+光照后复制 |
| **Fill（填充）** | 填充实色区域 | 无需采样源 |
| **Blur（模糊）** | 平滑细节层 | 模糊指定区域 |

### 重要技巧
- **圆形/椭圆**：点击拖动 = 目标位置，释放 = 源位置
- **画笔工具**：适合不规则形状（电线、树枝）
- **wavelet 分解**：分层处理，不同层处理不同细节级别
- **双实例法**：第一个去除大瑕疵，第二个做细节清理

---

## 十一、OpenCV 图像修复与无缝克隆

### Seamless Cloning
```python
output = cv2.seamlessClone(src, dst, mask, center, cv2.NORMAL_CLONE)
# src：源图（要克隆的物体）
# dst：目标图
# mask：大致轮廓（与src同尺寸）
# center：src中心在dst中的位置
# 模式：NORMAL_CLONE vs MIXED_CLONE
```

### Image Inpainting（去水印/划痕）
```python
# 1. 创建掩码（非0区域=需修复）
mask = cv2.imread('mask.png', 0)

# 2. 两种算法
result_telea = cv2.inpaint(img, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
result_ns = cv2.inpaint(img, mask, inpaintRadius=3, flags=cv2.INPAINT_NS)
# INPAINT_TELEA（推荐）：基于 Telea 算法，效果更好
# INPAINT_NS：基于 Navier-Stokes（流体动力学），有创意但易产生大区域模糊
```

---

## 十二、OpenCV 几何变换

### 旋转去歪斜
```python
coords = np.column_stack(np.where(gray > 0))
angle = cv2.minAreaRect(coords)[-1]
M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
```

### 透视变换
```python
pts1 = np.float32([[x1,y1], [x2,y2], [x3,y3], [x4,y4]])  # 源四边形
pts2 = np.float32([[0,0], [w,0], [w,h], [0,h]])           # 目标矩形
M = cv2.getPerspectiveTransform(pts1, pts2)
dst = cv2.warpPerspective(img, M, (w, h))
```

---

## 十三、OpenCV 全景拼接 & HDR

### 全景拼接
```python
stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)
status, pano = stitcher.stitch(images)
```

### Mertens 曝光融合（推荐！）
```python
merge_mertens = cv2.createMergeMertens()
fusion = (merge_mertens.process(images) * 255).astype(np.uint8)
# 不需要曝光时间！
```

---

## 十四、Python Pillow 拼贴画/水印/合成

### 拼贴画
```python
from PIL import Image, ImageOps
img = ImageOps.fit(img, cell_size, method=Image.LANCZOS)
collage.paste(img, (x, y))
```

### 水印
```python
# 透明水印
watermark.putalpha(130)
base.paste(watermark, position, mask=watermark)
```

---

## 十五、调色核心理论

### 调色流程（先定调后调色）
1. **先调光影**：曝光/阴影/高光先修好
2. **色温定调**：冷调 vs 暖调
3. **互补色公式**：黄蓝、青橙
4. **蓝原色校准**：左拉 → 青色

### 橙青风格实战步骤
1. 镜头校正 → 2. 降高光、提阴影 → 3. 蓝原色左拉 → 4. HSL 微调 → 5. 蒙版调肤色 → 6. 压暗边缘

### 分离色调
- 高光和阴影分别上色
- 饱和度建议 ≤ 20

---

## 十六、热门博主/资源推荐

### YouTube
- **Nigel Danson**（风景）、**Michael Shainblum**、**James Popsys**、**Thomas Heaton**

### 国内摄影师
- **林海音**（时尚）、**姜时一**（旅行）、**TKNORTH**（预设）

### Darktable 教程
- **Scott Gilbertson**（5.4 入门）、**Kevin Ajili**（sigmoid 工作流）
- **Avid Andrew**（Retouch 修销详解）
- 官方论坛：discuss.pixls.us

---

## 十七、关键心得

1. **修图不是炫技**：情感 > 参数
2. **降噪先于锐化**：顺序不能反
3. **Diffuse or Sharpen**：第四阶降噪最好（保边）
4. **Tone Equalizer**：按亮度区域调曝光，不是普通曲线
5. **双实例法**：处理复杂场景时分开调整更灵活
6. **HDR 接片**：曝光差大用 **Mertens Fusion**
7. **持续更新**：软件版本每半年大版本

---

## PS 2026 学习笔记（2026-04-10）

### 🔥 核心新功能
1. **Clarity + Dehaze 调整图层**（v27.3）：可对单个图层应用去雾/清晰度调节（以前只在 Camera Raw/Lightroom）
2. **Firefly 升级模型**：边缘更好、分辨率更高、人像生成更自然
3. **生成式扩展（Generative Expand）**：裁剪工具 → 透明 → Generative Expand，AI 补全背景
4. **增强版 Remove Tool**：AI 自动识别背景与人物主体，精准锁定多余元素
5. **AI 照片修复（Restore Photo）**：自动消除老照片划痕、折痕、磨损
6. **苹果芯片原生适配**：速度提升 50%+
7. **免费 Adobe Express 模板库**

### 📸 人像精修核心步骤（专业级）
1. **基础液化**：结构微调与对称性优化，不做"暴力拉脸"
2. **中性灰 + 频率分离**：还原干净肤质（不假面）
3. **Dodge & Burn**：强化光影结构感，五官更立体
4. **眼部细节精修**：眼神清晰度与明暗对比是关键
5. **整体色调统一**：Color Grading 决定"品牌感"

### 🎨 调色关键技巧
- 调整图层做局部色调分离
- LUT 文件做二级调色
- 曲线 + 色阶 + 色彩平衡 配合蒙版精准控制
- 冷暖色调分离：分区调整色温

### 🔑 重要博主/Tutorial资源
- **PiXimperfect**（Unmesh Dinda，5M订阅）：肤色校正、人像精修、Color Grading
- **PhotoshopCAFE**：每更新必出教程，去物体/修图强
- **Matt K**：Clarity/Dehaze 图层应用深度解析
- **PHLEARN**：Master Photoshop & Lightroom 2026 完整工作流
- **B站 - 敬伟PS教程**：中文入门到精通
- **B站 - 李涛摄影后期**：高质量调色原理

### 🔥 PS v27.5（2026年4月最新）新增功能
1. **Color & Vibrance 调整图层**：集温度/色调/饱和度于一身，直接在图层里修白平衡
2. **Rotate Object（3D变换）**：2D对象转可旋转3D视角，调整透视纵深
3. **Dynamic Text Shapes**：文字秒变圆形/弧形/蝴蝶结，路径可调、文字可编辑
4. **Topaz Gigapixel/Bloom 集成**：Image > Generative Upscale 内置顶级放大
5. **增强版 Remove Background**：复杂边缘（细发丝/精细纹理）识别更精准
6. **Harmonize**：自动协调色彩，让合成图色调统一自然
7. **Live Blend Mode Preview**：悬停即预览整图混合效果
8. **Firefly Boards 云文档互通**：云文档可投到 Firefly Boards 编辑后回传

### 🎬 电影感调色（Color Grading）核心技巧
**基础原理**：阴影偏青，高光/肤色偏橙——这是电影的标志性色调
**实现方法（Solid Color 调整图层）**：
1. 新建纯色图层（选择青蓝色）→ 混合模式 **Multiply** → 作用于阴影
2. 新建纯色图层（选择橙黄色）→ 混合模式 **Lighten** → 作用于高光
3. 用 **Blend If**（双击图层混合选项）精细控制影响范围

**曲线调色（Curves）关键用法**：
- RGB 通道：调整整体亮度对比
- 单通道（红/绿/蓝）：匹配肤色、修正白平衡
- 配合 **RGB Parade** 示波器监控

**快速电影感 90 秒大法**（PiXimperfect）：
Camera Raw → 基本调整 → HSL/颜色 → 分离色调（Split Toning）
