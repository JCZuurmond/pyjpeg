autoscale: true
slidenumbers: true
footer: Xccelerated session @ XKE 17-09-19

# [fit] Xccelerated

### Cor Zuurmond

![](../images/xccelerated.JPG "Xccelerated team")

---

# Xccelerated program

1. Bootcamp
2. At a company for a year
3. Comeback days
	- Hard skills
	- Soft skills

^ Company: Heineken
^ For me, a new thing was "knowledge sharing".

---

# [fit] Knowledge 
# [fit] sharing

^ 
Heineken COP: pandas time series and code quality  
Participate in the XKE

---


# [fit] Image compression

---

# What is compression?

![inline 150%](../images/xccelerated_small.JPG "Xccelerated team")

---

## Reducing the number of bits needed to store the image

---

# Naive compression
### Cropping the image

![inline 150%](../images/xccelerated_cropped.JPG "Xccelerated team")

**note:** 25% of original image

---

# Naive compression
### Clipping the pixel values

![inline 150%](../images/xccelerated_clipped.JPG "Xccelerated team")

**note:** 87.5% of original image

^ Values are clipped to be between 0 and 128

---

# Naive compression
### Reduce number of color channels

![inline 150%](../images/xccelerated_gray.JPG "Xccelerated team")

**note:** 33.3% of original image

---

# Image compression
### How it should be done according to the Joint Photographic Experts Group (JPEG).

^ Joint Photographic Experts Group

---

# JPEG compression

1. From RGB to YCbCr
1. Per color channel:
	2. Discrete cosine transform (DCT)
	3. Quantization
	4. Entropy compression

---

# JPEG compression

1. From RGB to YCbCr
1. Per color channel:
	2. **Discrete cosine transform (DCT)**
	3. Quantization
	4. Entropy compression

---

# What is the discrete cosine transform?

^ With the discrete cosine transform you get frequency data

---

# In math

Apply to each 8 by 8 patch:

$$
G_{u, v} = \frac{1}{4} \alpha(u) \alpha(v) \sum\limits^{7}_{x=0} \sum\limits^{7}_{y=0}
g_{x, y} cos\left[\frac{(2x + 1) u \pi}{16} \right]  cos\left[\frac{(2x + 1) v \pi}{16}\right]
$$

where $$g_{x, y}$$ are the pixel values. 

---

# The important parts

Summations over your pixel values 

$$
\sum\limits^{7}_{x=0} \sum\limits^{7}_{y=0} g_{x, y}
$$

And the cosine stuff

$$
cos\left[\frac{(2x + 1) v \pi}{16}\right]
$$

When combined, these extract **frequency signals**.

---

# Less math, more visuals
### 1D DCT filter

```python
dct_cos = lambda x, u: np.cos(((2 * x + 1) * u * np.pi) / 16)

spatial_frequency = 0
dct_values = dct_cos(np.arange(8), spatial_frequency).reshape(1, 8)

_, ax = plt.subplots(1, 1)
ax.matshow(dct_values, cmap='gray', vmin=-1, vmax=1)
for idx, val in enumerate(dct_values.flatten()):
    c = 'black' if val > 0 else 'white'
    ax.text(idx, 0, round(val, 1), va='center', ha='center', color=c)
ax.get_xaxis().set_ticks([])
ax.get_yaxis().set_ticks([])
plt.tight_layout()
```

--- 

# 1D DCT filter
### Spatial frequency of 0 (or $$ 0 \pi /16 $$)

![inline](../images/dct_1d_0.JPG) 

--- 

# 1D DCT filter
### Spatial frequency of 1 (or $$ 1 \pi / 16 $$ )

![inline](../images/dct_1d_1.JPG) 

--- 

# 1D DCT filter
### Spatial frequency of 2 (or $$ 2 \pi / 16 $$ )

![inline](../images/dct_1d_2.JPG) 

--- 

# 1D DCT filter
### Spatial frequency of 7 (or $$ 7 \pi / 16 $$ )

![inline](../images/dct_1d_7.JPG) 

--- 

# 2D DCT filter

```python
dct_cos = lambda x, u: np.cos(((2 * x + 1) * u * np.pi) / 16)

hor_spatial_frequency = 0
ver_spatial_frequency = 0
hor_dct_values = dct_cos(np.arange(8), hor_spatial_frequency)
ver_dct_values = dct_cos(np.arange(8), ver_spatial_frequency)
dct_values = np.outer(ver_dct_values, hor_dct_values)

_, ax = plt.subplots(1, 1)
ax.matshow(dct_values, cmap='gray', vmin=-1, vmax=1)
for u in range(8):
    for v in range(8):
        val = dct_values[u, v]
        c = 'black' if val > 0 else 'white'
        ax.text(v, u, round(val, 1), va='center', ha='center', color=c)
ax.get_xaxis().set_ticks([])
ax.get_yaxis().set_ticks([])
plt.tight_layout()
```

---

# 2D DCT filter
### Horizontal and vertical spatial frequencies of 0 and 0 (or $$ 0 \pi / 16 $$ and $$ 0 \pi / 16 $$ ), respectively

![inline](../images/dct_2d_0_0.JPG) 

---

# 2D DCT filter
### Horizontal and vertical spatial frequencies of 1 and 0 (or $$ 1 \pi / 16 $$ and $$ 0 \pi / 16 $$ ), respectively

![inline](../images/dct_2d_1_0.JPG) 

---

# 2D DCT filter
### Horizontal and vertical spatial frequencies of 2 and 0 (or $$ 2 \pi / 16 $$ and $$ 0 \pi / 16 $$ ), respectively

![inline](../images/dct_2d_2_0.JPG) 

---

# 2D DCT filter
### Horizontal and vertical spatial frequencies of 0 and 1 (or $$ 0 \pi / 16 $$ and $$ 1 \pi / 16 $$ ), respectively

![inline](../images/dct_2d_0_1.JPG) 

---

# 2D DCT filter
### Horizontal and vertical spatial frequencies of 0 and 2 (or $$ 0 \pi / 16 $$ and $$ 2 \pi / 16 $$ ), respectively

![inline](../images/dct_2d_0_2.JPG) 

---

# 2D DCT filter
### Horizontal and vertical spatial frequencies of 1 and 1 (or $$ 1 \pi / 16 $$ and $$ 1 \pi / 16 $$ ), respectively

![inline](../images/dct_2d_1_1.JPG) 

---

# 2D DCT filter
### Horizontal and vertical spatial frequencies of 2 and 2 (or $$ 2 \pi / 16 $$ and $$ 2 \pi / 16 $$ ), respectively

![inline](../images/dct_2d_2_2.JPG) 

---

# 2D DCT filter
### Horizontal and vertical spatial frequencies of 3 and 6 (or $$ 3 \pi / 16 $$ and $$ 6 \pi / 16 $$ ), respectively

![inline](../images/dct_2d_3_6.JPG) 

---

# 2D DCT filter
### Horizontal and vertical spatial frequencies of 7 and 7 (or $$ 7 \pi / 16 $$ and $$ 7 \pi / 16 $$ ), respectively

![inline](../images/dct_2d_7_7.JPG) 

---

# All 2D DCT filters; All basis filters

![inline 70%](../images/dct_grid.JPG)

---

## DCT decomposes a patch as a linear combination of the basis filters

![inline](../images/patch.JPG) ![inline 70%](../images/dct_grid.JPG)

---

# Why do we want frequencies?

^ We are less sensitive too high frequency changes than low frequency changes.

---

# An example

![inline](../images/patch_numbers.jpg) 

---

# We center it around zero 
### by subtracting 127

![inline](../images/patch_shifted_numbers.jpg) 

---

# We apply DCT to get

![inline](../images/patch_dct.jpg) 

---

## Pixel domain --> frequency domain

![inline](../images/patch_shifted_numbers.jpg) ![inline 80%](../images/dct_grid_w_numbers.JPG)

^ Top left is the DC coefficient (constant hue)
^ The others are the AC coefficient (altering components)

---

# JPEG compression

1. From RGB to YCbCr
1. Per color channel:
	2. Discrete cosine transform (dct)
	3. **Quantization**
	4. Entropy compression


---

# Quantization
### Divide and round the DCT coefficients by some factors. 

![inline](../images/patch_dct.jpg) 

The goal is to have many zeros at the end.

^ JPEG pre-defined quantization matrices, which are linked with the quality.

---

# JPEG compression

1. From RGB to YCbCr
1. Per color channel:
	2. Discrete cosine transform (dct)
	3. Quantization
	4. **Entropy compression**

^ End of block and less bits for numbers that occurred more often

---

# Code is on Github

### https://github.com/JCZuurmond/pyjpeg

![](../images/xccelerated.JPG "Xccelerated team")

^ According to Wikipedia: JPEG typically achieves 10:1 compression with little perceptible loss in image quality

