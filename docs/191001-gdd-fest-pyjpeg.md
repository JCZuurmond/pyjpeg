slidenumbers: true
footer: Implementing JPEG in Python | Open Source Day, GoDataFest 2019, Cor Zuurmond | github.com/JCZuurmond/pyjpeg

# Implementing 
# [fit] JPEG 
# in Python

---

# Meet Lena

![inline](pictures/stick-figure3.png)

---

# She is a data consultant

![inline](pictures/stick-figure3.png)

---

## Lena dreamt of going back in time

![inline](pictures/clock-going-back2.png)

---

# She would be a data queen[^0]

![inline](pictures/stick-figure-king.png)

[^0]: Crown by Marco Livolsi from the Noun Project

---

# Just another day 

![inline](pictures/stick-figure3.png)

---

# New client

![inline](pictures/building.png)

---

# Something special happened

![inline](pictures/elevator.png)

---

# Lena did not notice it at first

![inline left](pictures/stick-figure3.png)

^ 
Sure people look old and fancy
She walked to the meeting room and told everybody the
data consultant was here!

---

# The data consultant is here!

![inline left](pictures/stick-figure3.png)

---

# Peet was skeptical

![inline left](pictures/stick-figure3.png) ![inline right](pictures/stick-figure-hat.png)

[.header: alignment(right)]

---

## His company invested a lot of money in digital photo cameras


![inline left](pictures/stick-figure3.png) ![inline right](pictures/stick-figure-hat.png)

[.header: alignment(right)]

---

# [fit] Can you help us?

---

# Did you compress your images?

![inline](pictures/stick-figure3.png)

---

# Compress?

![inline left](pictures/stick-figure3.png) ![inline right](pictures/stick-figure-hat.png)

[.header: alignment(right)]

---

# Yes, compress!

![inline left](pictures/stick-figure3.png) ![inline right](pictures/stick-figure-hat.png)

---

# [fit] .zip 
# [fit] .tar
# [fit] .gz
# [fit] deflate

---

# Compress!

![inline left](pictures/stick-figure3.png) ![inline right](pictures/stick-figure-hat.png)

---

# No... Can you do it?

![inline left](pictures/stick-figure3.png) ![inline right](pictures/stick-figure-hat.png)

[.header: alignment(right)]

---

# Uhm, sure!

![inline left](pictures/stick-figure3.png) ![inline right](pictures/stick-figure-hat.png)

---

## As always, Lena started with Google

---

# but Google did not work.

---

# Lena found out she time traveled

![inline](pictures/stick-figure3.png)

---

# After a 
# [fit] mental breakdown 
# of a couple hours

---

# How does image compression work?

---

# She thought hard <br> and hard

---

## The next day she presented her findings

![inline](pictures/stick-figure3.png)

----

# Original image

![inline 250%](pictures/lena.png)

----

# Original image

![inline](pictures/lena-dimensions-channels.png)

---

# Number of bits

$$N_{\textit{pixels}} = W * H * C$$
<br>
$$N_{\textit{bits}} = N_{\textit{pixels}} * \textit{pixels per bit}$$

$$W$$ = width
$$H$$ = height
$$C$$ = channels

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

## I am a little disappointed

![inline left](pictures/stick-figure3.png) ![inline right](pictures/stick-figure-hat.png)

^
To put it softly

[.header: alignment(right)]

---

## Can I have a second chance?

![inline left](pictures/stick-figure3.png) ![inline right](pictures/stick-figure-hat.png)

---

# Lena needed a drink

![inline](pictures/stick-figure3.png)

^
After sitting in the bar for a couple hours staring blank to the wall.

---

## Lena was not the data queen she thought she would be[^0]

![inline](pictures/stick-figure-king-unhappy.png)

---

# She was standing <br> on the <br> shoulders of giants

---

## Mr Huffman walked into the bar

![inline 250%](pictures/stick-figure-old.png)

^ 
Why the long face?
Lena told about the compression. Mr Huffman did not know anything about image
compression. But she knew about the war.

---

# He started talking about the war

---

## He told about Morse code

![inline 250%](pictures/stick-figure-old.png)

^
She sent messages about the weather. And that they had special codes for the
common weather types. Also they thought off a code to get more cigarettes and
beer.

---

## More frequently occurring characters get shorter codes

![inline](pictures/morse-code.png)

---

# What if more frequently occurring pixel values use less bits?

---

# This might work!

![inline](../images/lena-pixel-values-hist.png)

---

# Though...

- Probably other pictures have a different distribution in pixel values;

---

# Though...

- Probably other pictures have a different distribution in pixel values;
- Storing the mapping (every time) takes memory;

---

# Though...

- Probably other pictures have a different distribution in pixel values;
- Storing the mapping (every time) takes memory;
- We do not know the distribution of pixel values of all images;

---

# Though...

- Probably other pictures have a different distribution in pixel values;
- Storing the mapping (every time) takes memory;
- We do not know the distribution of pixel values of all images;
- The distribution might be mostly flat - equally distributed.

---

## Lena felt she was on the right track

![inline](pictures/stick-figure3.png)

---

# What do all pictures have in common?

---

# Let's look at the image again

![inline](pictures/lena.png)

---

# Neighbouring pixels

![inline](pictures/lena-areas.png)

---

# Most pixels have similar values as their neighbouring pixels

---

# Lena got in the flow

1. If pixels are correlated to neighbouring pixels,

---

# Lena got in the flow

1. If pixels are correlated to neighbouring pixels,
   the change in values of neighbouring pixels is low.

---

# Lena got in the flow

1. If pixels are correlated to neighbouring pixels,
   the change in values of neighbouring pixels is low.
2. If we decompose pictures into frequencies,

---

# Lena got in the flow

1. If pixels are correlated to neighbouring pixels,
   the change in values of neighbouring pixels is low.
2. If we decompose pictures into frequencies,
   we expect mostly low frequencies, and few high frequencies.

---

# Lena got in the flow

1. If pixels are correlated to neighbouring pixels,
   the change in values of neighbouring pixels is low.
2. If we decompose pictures into frequencies,
   we expect mostly low frequencies, and few high frequencies.
3. The factor of high frequencies is low - probably zero.

---

# Lena got in the flow

1. If pixels are correlated to neighbouring pixels,
   the change in values of neighbouring pixels is low.
2. If we decompose pictures into frequencies,
   we expect mostly low frequencies, and few high frequencies.
3. The factor of high frequencies is low - probably zero.
4. We can compress many zeros!

---

# How to get pixel value frequencies?

---

# Convolution?
# Filters?

---

# Filters

---

# Filters extract certain frequencies

---

# Cookiecutter

![inline 250%](pictures/cookie-cutter.png)

^
The shape - filter - you have determines what you get out.

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

# Convolution

---

# A convolution applies a filter to a group of <br> neighbouring pixels

---

# It loops over groups of pixels[^1]

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

# All together

<br>

```
for each filter:
	for each group of pixels:
		apply filter to the group of pixels
```

---

# This is what Lena did!

![inline](pictures/stick-figure3.png)

---

# Original image

![inline](../images/lena.png)

---

# Image after applying the filters

![inline](../images/lena-freq.png)

---

# Side by side

![inline 250%](pictures/lena-freq.png)

---

# Side by side

![inline 250%](pictures/lena-freq-areas.png)

---

# Most values were around zero!

![inline](../images/lena-compressed-pixel-values-hist.png)

---

# If many values <br> are zero we can <br> compress them!

---

## We can get more zeros by removing high frequencies

---

# Remember the filters?

![inline](../images/dct_2d_0_0.png)

---

# Remember the filters?

![inline](../images/dct_2d_1_0.png)

---

# Remember the filters?

![inline](../images/dct_2d_7_0.png)

---

# Remember the filters?

![inline](../images/dct_2d_0_1.png)

---

# Remember the filters?

![inline](../images/dct_2d_0_3.png)

---

# Remember the filters?

![inline](../images/dct_2d_0_7.png)

---

# Remember the filters?

![inline](../images/dct_2d_1_1.png)

---

# Remember the filters?

![inline](../images/dct_2d_3_3.png)

---

# Remember the filters?

![inline](../images/dct_2d_5_2.png)

---

# Remember the filters?

![inline](../images/dct_2d_3_6.png)

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

# Reduce higher frequencies with a bigger factor

---

# Reduce matrix

![inline](pictures/quantization-dimensions.png) 

---

# Reduce matrix

![inline](pictures/quantization-dimensions-areas.png) 

---

# Lena put it all together

---

# Original image

![inline](../images/lena.png)

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

# With a reduction of 85%!!!!!

---

## Peet was very happy!

![inline](pictures/stick-figure-hat-happy.png)

---

## Lena was a data queen after all!!![^0]

![inline](pictures/stick-figure-king.png)

---

# Open Source <br> makes life easier

---

# Implementing 
# [fit] JPEG 
# in Python

---

# Code is on Github

# [fit] github.com/JCZuurmond/pyjpeg
