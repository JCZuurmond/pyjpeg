slidenumbers: true
footer: PyData Meetup 26-02-20, Image compression

# Image compression
# in Python

----

# Learn how to compress the following image

![inline 200%](pictures/lena.png)

---

# Before we start coding

---

# Let's discuss quantities of data

- Big data;
- Small data;
- Huge data;
- Tiny data;
- Enormous data;

---

# Let's discuss quantities of data

- Big data;
- Small data;
- Huge data;
- Tiny data;
- Enormous data;

----

# You want big data?

![inline](pictures/lena-twice.png)

---

# Big data you will get

![inline](pictures/lena-hundred.png)

---

# When do we have "more" data?

---

# When do we have "more" data?

- Not just more samples

---

# When do we have "more" data?

- Not just more samples;
- The samples should be different from each other;

---

# But, this is not useful either

![inline](pictures/lena-rot.png)

---

# When do we have "more" data?

- Not just more samples;
- ~~The samples should be different from each other;~~
- The samples should contain different "information";

---

# But, this is not useful either

![inline](pictures/lena-noise.png)

---

# When do we have "more" data?

- Not just more samples;
- ~~The samples should be different from each other;~~
- ~~The samples should contain different "information";~~
- The samples should contain different "useful information";

---

# Useful information

- Different meaning for:
	- Different types of data;
	- Different uses for the data;

---

# Useful information

- Different meaning for:
	- **Different types of data;**
	- Different uses for the data;

---

# Images

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

# What is <br> "useful information" within images?

---

# Images are autocorrelated data

![inline](pictures/lena-areas.png)

---

# We need to go to the frequency domain!

---

# Discrete cosine transform

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

