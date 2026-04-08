# Darktable 修图技巧笔记

## 核心工作流（scene-referred）

### 1. 基础调整（Base 模块组）

**曝光（Exposure）**
- 调整中间调灰度到合适亮度
- 用吸管点击画面中应该是灰色的区域自动校正
- 不要过度关注高光/暗部，后续会处理

**白平衡（Color Calibration）**
- 第一个 Color Calibration 实例只用来校白平衡
- 其他调色用新的独立实例
- 用"自动"或吸管在画面中找中性灰/白点

### 2. 色调映射

**Filmic RGB 或 Sigmoid**
- Filmic：适合写实风格，控制动态范围
- Sigmoid：更适合让颜色"弹出来"，对初学者友好
- 新手推荐 Sigmoid

**Tone Equalizer**
- 几乎每张照片都要用
- 分别调整高光/中间调/暗部的对比度

### 3. 对比度与清晰度

**Color Balance RGB**
- 全局自然饱和度（vibrance）拉高一点
- 饱和度（saturation）按需加
- 对比度调节（shadows/midtones/highlights）
- 颜色分级（color grading）做创意调色

**Diffuse or Sharpen**
- 锐化用"lens deblur | medium"预设
- 局部对比度用"contrast equalizer clarity"预设

### 4. 降噪与镜头校正

**Denoise (profiled)**
- 依赖相机配置文件
- 高 ISO 照片必备

**Lens Correction**
- 去除暗角和畸变
- 自动从镜头配置读取

### 5. 裁剪与构图

**Crop**
- 先裁再调色
- 叠加辅助线（九宫格等）

## 常用模块优先级

**必备：**
1. Exposure
2. Color Calibration（白平衡）
3. Denoise / Lens Correction（技术校正）
4. Crop
5. Tone Equalizer
6. Color Balance RGB

**进阶可选：**
- Retouch：修瑕疵/杂物
- Color Zones：分区调色
- Contrast Equalizer：局部对比
- LUT 3D：调色 LUT
- Diffuse or Sharpen：锐化

## 快捷技巧

- **Shift+E**：快速调曝光（可在设置里绑定）
- **快照对比**：在编辑过程中点快照，方便对比不同调色效果
- **复制到多张**：在 Lighttable 选中多张图，"样式"批量应用
- **蒙版调色**：用亮度/形状蒙版做局部调整

## 调色顺序建议

1. 技术校正（降噪、镜头校正、裁剪）
2. 基础曝光
3. 白平衡校准
4. 色调映射（filmich 或 sigmoid）
5. 对比度和清晰度
6. 颜色饱和度/自然饱和度
7. 创意颜色分级
8. 锐化输出

## 学习资源

- Bruce Williams Photography（YouTube）：理解 Darktable 系列
- darktable 官方文档：docs.darktable.org
- pixls.us 社区论坛：discuss.pixls.us
- Andrew Raub's beginner workflow（darktable.org 官方博客）
