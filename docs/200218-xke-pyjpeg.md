slidenumbers: true
footer: PyData Meetup 26-02-20, Image compression

# Efficiently store your images

----

# Today we own a webshop

----

# Webshop

- Not a small one, but one of similar size as Alibaba or Amazon;

----

# Webshop

- Not a small one, but one of similar size as Alibaba or Amazon;
- People upload thousands of photos every day;
	- They need to be stored;
	- Send to people who request them;

---

# A lot of data (movement) <br> is involved with these images

---

# We are responsible for handling this efficiently

---

# We are responsible for handling this efficiently
## A.k.a. save money 

---

## Let's discuss some obvious examples

![inline](pictures/lena-twice.png)

^ Some duplicates might be needed to avoid data loss and have short response
time across the globe

---

## Unnecessary duplicates can be removed!

![inline](pictures/lena-hundred.png)

---

# Only relevant images are kept

![inline](pictures/lena-noise.png)

---

## The question is: <br>What is useful information?

- Not useful are:
	- unnecessary duplicate values;
	- "meaningless" signals;

---

## Besides removing pictures as a whole, can we discard information within a picture?

---

# Can we compress images?

---

# How (not) to compress images

![inline 200%](pictures/lena.png)

----

# Image dimensions

![inline](pictures/lena-dimensions-channels.png)

---

# Number of bits

$$N_{\textit{pixels}} = W \cdot H \cdot C$$
<br>
$$N_{\textit{bits}} = N_{\textit{pixels}} \cdot \textit{pixels per bit}$$

$$W$$ = width
$$H$$ = height
$$C$$ = channels

![right 200%](pictures/lena-dimensions-channels.png)

---

# Pixel values

![inline 300%](pictures/pixel-values.png)

---

# Bits per pixel

![inline 250%](pictures/two-power-8.png)

---

## Number of bits
<br>
# $$ N_{\textit{bits}} = 8 * W * H $$
<br>
**Assuming grey pictures (1 channel)**

---

# Reduce image size with 37.5%!

![inline 300%](pictures/pixel-values-31.png)

---

# Compressed image I 

![inline](../images/lena-pixels-8.png)

---

# Reduce image size with 50%!!

![inline 300%](pictures/pixel-values-15.png)


---

# Compressed image II

![inline](../images/lena-pixels-16.png)

---

# Reduce image size by 75%!!!

---

# Compressed image III

![inline](../images/lena-quarter.png)

---

# So, how should we compress images?

---

![inline](../images/schematic-compression.png)

---

![inline](../images/schematic-compression-perfect.png)

---

![inline](../images/schematic-compression-naive.png)

---

![inline](../images/schematic-compression-better.png)

---

![inline](../images/schematic-compression-ok.png)

---

# So, how to compress images?

- maybe we can do something with:
	- duplicate values;
	- "meaningless" signals;

---

# "Duplicate" values

![inline](pictures/lena-areas.png)

---

# Images are autocorrelated

---

# Downsampling 
## 6% of original image size

![inline](../images/lena-downsampled-4.png)

---

# Downsampling
## 1.5% of original image size

![inline](../images/lena-downsampled-8.png)

---

# Can we extract these autocorrelated signals?

---

# Maybe with frequencies!

---

# Discrete cosine transform


---

# Convolution[^1]

![inline](https://neurohive.io/wp-content/uploads/2018/07/convolutional-neural-network.gif)

[^1]: https://zhenye-na.github.io/2018/11/30/cnn-deep-leearning-ai-week1.html

---

# An example[^2]

![inline](https://miro.medium.com/max/1026/1*cTEp-IvCCUYPTT0QpE3Gjg@2x.png)


[^2]: https://towardsdatascience.com/applied-deep-learning-part-4-convolutional-neural-networks-584bc134c1e2

---

# An example[^2]

![inline](https://cdn-media-1.freecodecamp.org/images/Htskzls1pGp98-X2mHmVy9tCj0cYXkiCrQ4t)

^ https://towardsdatascience.com/applied-deep-learning-part-4-convolutional-neural-networks-584bc134c1e2


---

# Filter that resembles a wave

![inline](../images/wave-1.png)

---

# A filter for each frequency

![inline](../images/wave-1.5.png)

---

# Another frequency

![inline](../images/wave-2.png)

---

# Another frequency

![inline](../images/wave-3.png)

---

# But, for pictures/pixels

<br> <br>

![inline](../images/dct_1d_1.png)

---

# Another frequency

<br> <br>

![inline](../images/dct_1d_2.png)

---

# Another frequency

<br> <br>

![inline](../images/dct_1d_3.png)

---

# Another frequency

<br> <br>

![inline](../images/dct_1d_4.png)

---

# Filter for zero frequency

<br> <br>

![inline](../images/dct_1d_0.png)

---

# Two-dimensional filter

![inline](../images/dct_2d_0_0.png)

---

# Changing horizontal frequency

![inline](../images/dct_2d_1_0.png)

---

# Changing horizontal frequency

![inline](../images/dct_2d_2_0.png)

---

# Changing horizontal frequency

![inline](../images/dct_2d_3_0.png)

---

# Changing horizontal frequency

![inline](../images/dct_2d_7_0.png)

---

# Changing vertical frequency

![inline](../images/dct_2d_0_1.png)

---

# Changing vertical frequency

![inline](../images/dct_2d_0_2.png)

---

# Changing vertical frequency

![inline](../images/dct_2d_0_3.png)

---

# Changing vertical frequency

![inline](../images/dct_2d_0_7.png)

---

# Changing both frequencies

![inline](../images/dct_2d_1_1.png)

---

# Changing both frequencies

![inline](../images/dct_2d_2_2.png)

---

# Changing both frequencies

![inline](../images/dct_2d_3_3.png)

---

# Or

![inline](../images/dct_2d_5_2.png)

---

# Or

![inline](../images/dct_2d_3_6.png)

---

# High frequency

![inline](../images/dct_2d_7_7.png)

---

# Frequency values

![inline](../images/image-frequencies-pixel-values.png)

---

## Here we see more duplicates! 
### There are many zeros

![inline](../images/image-frequencies-pixel-values.png)

---

# We can use this in our encoding

--- 

![inline](pictures/encode-values.png)

---

# So, how to compress images?

- maybe we can do something with:
	- ~~duplicate values;~~
	- "meaningless" signals;

---

# Remember the filters?

![inline](../images/dct_2d_7_7.png)

---

![300%](pictures/all-filters.png)

--- 

![300%](pictures/all-filters-dimensions.png)

---

![300%](pictures/all-filters-crossed.png)

---

# Remove higher frequencies

---

# Reduce matrix

![inline](pictures/quantization-dimensions.png) 

---

# Reduce matrix

![inline](pictures/quantization-dimensions-areas.png) 

---

# Skip the implementation of the reverse logic

---

# Compressed image

![inline](../images/lena-jpg.png)

---

# Side by side

![inline 300%](pictures/lena-side-by-side.png)

---

# Side by side

![inline 300%](pictures/lena-side-by-side-areas.png)

--- 

# With a reduction of 85%!!!
