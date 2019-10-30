slidenumbers: true
footer: Implementing JPEG in Python | GoDataFest 2019, Cor Zuurmond | github.com/JCZuurmond/pyjpeg

# Implementing 
# [fit] JPEG 
# in Python

---

# Meet lena

![inline](pictures/stick-figure3.png)

---

# She is a data consultant

![inline](pictures/stick-figure3.png)

---

# Lena dreamt of going back in time

![inline](pictures/clock-going-back2.png)

---

# She would be data queen

![inline](pictures/stick-figure-king.png)

^ Crown by Marco Livolsi from tshe Noun Project

---

# And just that happened to Lena...

![inline](pictures/stick-figure3.png)

---

# just another day 

![inline](pictures/stick-figure3.png)

---

# New client

![inline](pictures/building.png)

---

# Something special happened

![inline](pictures/elevator.png)

---

# It was not just an elevator, it also was a time machine

![inline](pictures/clock-going-back2.png)

---

# Lena did not notice at first

![inline](pictures/stick-figure3.png)

^ 
Sure people look old and fancy
She walked to the meeting room and told everybody the
data consultant was here!

---

## Peet was skeptical, but he needed Lenas help!

![inline](pictures/stick-figure-hat.png)

---

## Her company invested a lot of money in digital photo cameras. 

![inline](pictures/stick-figure-hat.png)

---

# [fit] Can you help us?

---

# Did you compress your images?

![inline](pictures/stick-figure3.png)

---

# Compress?

![inline](pictures/stick-figure-hat.png)

---

# Yes, compress!

![inline](pictures/stick-figure3.png)

---

# [fit] .zip .tar
# [fit] .gz
# [fit] deflate
# [fit] compress

---

# No... Can you do it?

![inline](pictures/stick-figure-hat.png)

---

# Uhm, sure!

![inline](pictures/stick-figure3.png)

---

## As always, Lena started with google

---

# but google did not work.

---

# Lena found out she time traveled

![inline](pictures/stick-figure3.png)

---

# After a 
# [fit] mental breakdown 
# of a couple hours

---

## Lena was back to being her normal self

![inline](pictures/stick-figure3.png)

---

# How does images compression work?

---

# She thought hard <br> and hard

---

# She presented her findings

![inline](pictures/stick-figure3.png)

----

# Original image

![inline 250%](pictures/lena.png)

----

# Original image

![inline](pictures/lena-dimensions.png)

---

# Number of bits

![inline 300%](pictures/image-bits.png)

---

# Pixel values

![inline 300%](pictures/pixel-values.png)

---

# Bits per pixel

![inline 250%](pictures/two-power-8.png)

---

# Number of bits

![inline 300%](pictures/image-bits-final.png)

---

# Reduce image size with 37.5%!

![inline 300%](pictures/pixel-values-32.png)

---

# Compressed image I 

![inline](../images/lena-pixels-8.png)

---

# Reduce image size with 50%!

![inline 300%](pictures/pixel-values-16.png)

---

# Compressed image II

![inline](../images/lena-pixels-16.png)

---

# Reduce image size by 75%!!!

---

# Compressed image III

![inline](../images/lena-quarter.png)

^
To put it softly:

---

# Peet was a little disappointed

![inline](pictures/stick-figure-hat.png)

^
Which Lena understood

---

# Lena asked for a second chance

![inline](pictures/stick-figure3.png)

---

## Lena went to a bar for a drink and to think

![inline](pictures/stick-figure3.png)

^
After sitting in the bar for a couple hours staring blank to the wall.

---

## Mr Huffman walked into the bar

![inline 250%](pictures/stick-figure-old.png)

^ 
Why the long face?
Lena told about the compression. Mr Huffman did not know anything about image
compression. But she knew about the war.

---

# She started talking about the war

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
- Remembering the mapping (every time) takes memory;

---

# Though...

- Probably other pictures have a different distribution in pixel values;
- Remembering the mapping (every time) takes memory;
- We do not know the distribution of pixel values of all images;

---

# Though...

- Probably other pictures have a different distribution in pixel values;
- Remembering the mapping (every time) takes memory;
- We do not know the distribution of pixel values of all images;
- The distribution might be mostly flat - equally distributed.

---

## Lena knew she was on the right track

![inline](pictures/stick-figure3.png)

---

# What do all pictures in common?

---

# Neighbouring pixels

![inline](pictures/lena-areas.png)

---

# Pixels have similar values as their neighbouring pixels

---

# Lena got in the flow

1. If, pixels are correlated to neighbouring pixels;

---

# Lena got in the flow

1. If, pixels are correlated to neighbouring pixels;
2. The change in values of neighbouring pixels is low;

---

# Lena got in the flow

1. If, pixels are correlated to neighbouring pixels;
2. The change in values of neighbouring pixels is low;
3. A.k.a. the pixel value _frequency_ of neighbouring pixels is low;

---

# Lena got in the flow

1. If, pixels are correlated to neighbouring pixels;
2. The change in values of neighbouring pixels is low;
3. A.k.a. the pixel value _frequency_ of neighbouring pixels is low;
4. We need a low pass filter for the pixel values frequencies!

---

# Lena got in the flow

1. If, pixels are correlated to neighbouring pixels;
2. The change in values of neighbouring pixels is low;
3. A.k.a. the pixel value _frequency_ of neighbouring pixels is low;
4. We need a low pass filter for the pixel values frequencies!

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

# Highest frequency

![inline](../images/dct_2d_7_7.png)

--- 

# Convolution

---

# A loop over group of pixels

![inline](https://neurohive.io/wp-content/uploads/2018/07/convolutional-neural-network.gif)

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

# Most values were around zero

![inline](../images/lena-compressed-pixel-values-hist.png)

---

# The final step Lena needed to do is the _low pass_ part

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

# Reduce higher frequency with a bigger factor

---

# Reduce matrix

![inline](pictures/quantization-dimensions.png) 

---

# Lena put it all together

---

# Original image

![inline](../images/lena.png)

---

# Compressed image

![inline](../images/lena-jpg.png)

---

# Side to side

![inline 100%](../images/lena-side-to-side.png)

---

# With a reduction of 85%!!!!!

---

## Peet was very happy!

![inline](pictures/stick-figure-hat-happy.png)

---

# Lena was a data queen!!!

![inline](pictures/stick-figure-king.png)

---

# Implementing 
# [fit] JPEG 
# in Python