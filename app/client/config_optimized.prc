# Kitaverse Mobile Optimization Configuration

[general]
# Reduce overall quality for better performance
model-cache-dir=.
model-cache-textures=1

[graphics]
# Graphics settings optimized for low-end devices
framebuffer-multisample=0
multisamples=0
compressed-textures=1
textures-power-2=1
textures-auto-compress=1
textures-quality=low
textures-scale=0.5

# Reduce rendering quality
lod-distance=50
lod-levels=2
occlusion-culling=1
render-yield-time=0.01

[audio]
# Audio settings
audio-library-name=null