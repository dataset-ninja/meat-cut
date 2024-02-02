The aim of **Meat Cut Image Dataset (BEEF)** creation was to identify five different meat cuts from images and weights collected by a trained operator within the working environment of a commercial Irish beef plant. Individual cut images and weights from 7,987 meats cuts extracted from semimembranosus muscles (i.e., topside muscle), post editing, were available.

## Motivation

The identification of different meat cuts for labeling and quality control on production lines is still largely a manual process. As a result, it is a labor-intensive exercise with the potential for not only error but also bacterial cross-contamination. Artificial intelligence is used in many disciplines to identify objects within images, but these approaches usually require a considerable volume of images for training and validation. Processes such as meat cutting, fat determination, and meat deboning have been partially automated. However, the labeling and identification of meat cuts still require a substantial amount of human intervention and manual handling. This can incur additional labor costs as well as being a source of error and potential microbiological contamination. Primal boning lines are a typical example of where multiple operators simultaneously work on a range of meat cuts. Each cut will eventually arrive at a weighing station where a single operator will inspect, identify, and weigh the arriving meat cut. The automation of the weighing process on boning lines has traditionally been conducted on single-meat-cut production lines. However, due to spatial restrictions in many meat plants, there is a preference in the beef industry to operate multiple meat cut types simultaneously on a single processing line. 

## Dataset creation

The data collected for this project were from beef cuts taken from a Topside (i.e., semimembranosus muscle) trimming line of a major Irish beef processor. The process flow for this line required an operator to weigh the primal topside cut on a start-of-line (SOL) weighing scales. Each cut was then placed on a conveyor belt where a team of operators removed fat, gristle, and secondary muscles. The remaining meat cuts were then labeled, weighed, and an image captured by a trained operator on an end-of-line (EOL) weighing scales, where the meat cuts were vacuum packed and labeled. For this dataset, there were five different meat cuts derived from the topside primal. The data acquisition required a hardware setup of weighing scales, at both the SOL and EOL together with a Vivotek bullet camera (IP8362—Bullet–Network Camera) at the EOL to capture a photo image of each meat cut. In addition, bespoke data capture software was used to acquire the characteristics of each meat cut being weighed in a 4-step process.

1) A manual capture of the carcass identifier number, primal weight, and the time of arrival at the SOL scales.
2) The time and the id of the operator validating the meat cut image as well as the meat cut weight, meat cut label, and a photo image at the EOL scales were all captured on bespoke data capture software used as a form of data acquisition in the development of an Agri Data Warehouse.
3) The EOL operator identified the meat cut using the data capture interface, ensuring the correct image was stored to disk and linked to the appropriate database entry containing the variables captured at both EOL and SOL points.
4) After each meat cut was removed from the scales, an image of the empty scales was captured. This was done to help remove image noise (discussed later).

<img src="https://github.com/dataset-ninja/meat-cut/assets/120389559/c03d32f9-14fb-453a-b357-0cf0f3a95534" alt="image" width="1000">

<span style="font-size: smaller; font-style: italic;">Topside cuts: five meat cut variations. (a) Cap Off Pear Off, PAD topside muscle (20001); (b) Cap off, Pear on topside muscle (20002); \(c\) Topside Heart muscle (20003); (d) Topside Bullet muscle (20004); and (e) Cap Off, Non-PAD, Blue Skin Only topside muscle (20010).</span>

<img src="https://github.com/dataset-ninja/meat-cut/assets/120389559/e7377895-8696-47a6-b9ed-de28f2762982" alt="image" width="1000">

<span style="font-size: smaller; font-style: italic;">End of line (EOL): a user interface for data collection.</span>

A trained operator identified the meat cuts for subsequent categorization; the cuts were categorized as: 
* ***cap off pear off, pad topside muscle*** 
* ***cap off, pear on topside muscle***
* ***topside heart muscle***
* ***topside bullet muscle***
* ***cap off, non-pad, blue skin only topside muscle***

| Meat cut ID | N    | Meat cut description                | X−±S            | Cut yield, % |
|-------------|------|-------------------------------------|-----------------|--------------|
| 20001       | 1,060| Cap Off, Pear Off, PAD              | 6.47 ± 1.17     | 55.11        |
| 20002       | 14   | Cap Off, PAD On                     | 8.87 ± 0.98     | 68.18        |
| 20003       | 2,132| Topside Heart PAD                   | 5.87 ± 1.10     | 44.00        |
| 20004       | 2,085| Topside Bullet                      | 1.40 ± 0.29     | 9.45         |
| 20010       | 2,696| Cap Off Non-PAD Blue Skin Only      | 7.82 ± 1.59     | 61.55        |


<span style="font-size: smaller; font-style: italic;">Dataset summary statistics.</span>

The data collection period lasted 3 weaks. At the end of the data collection period, an analysis was conducted to determine if there were any outlying weights; this was undertaken by comparing the weights of the primal cut weighed on the SOL scales with the weight of the corresponding generated meat cut on the EOL scales. The ratio of each meat cut weighed on the EOL relative to the primal cut on the SOL is known as the product yield. Boning operators generally have target product yields which are dependent on the product specification. As the beef plant operator had a specification limit of 10.00% for each of the meat cuts used in these experiments, any absolute difference between the actual product yield and the target product yield that exceeded 10.00% was flagged as an outlier and subsequently removed from the dataset.

## Image preprocessing

When conducting image preprocessing, one generally aims to improve the prediction process by enhancing certain characteristics and/or blurring others. For this dataset, each meat cut image was accompanied by its associated background image. In order to remove distracting or confusing items (e.g., operator hands or small meat blobs), the background image was removed from the meat cut image. This image was then converted to grayscale, and finally, the meat cut was segmented from the scale using the Gaussian blur technique. This final set of original and grayscale images was used in the model construction.

<img src="https://github.com/dataset-ninja/meat-cut/assets/120389559/de145d25-6618-4188-aef7-9fad1bef0896" alt="image" width="1000">

<span style="font-size: smaller; font-style: italic;">Images at various stages of preprocessing: (a) The background image reflecting the scale on which the meat cuts were placed, (b) the scale with a meat cut on it, \(c\) the difference between image (a) and (b), (d) the grayscale conversion of image \(c\), and (e) image represents the segmented meat cut.</span>

The frequency of meat cut 20002 was disproportionately low as it is not frequently harvested in this plant. Therefore, it was decided to use data augmentation to create artificial training samples for meat cut 20002 in order to improve the imbalanced nature of the dataset. As part of the augmentation process, transformations such as anticlockwise rotation, clockwise rotation, horizontal flip, vertical flip, noise addition, and blurring were implemented. These processes created 84 additional images for meat cut 20002 resulting in a final count of 98 images. 

**Note**: the authors of the dataset did not provide a way to compare <i>Weights</i> with the corresponding image.
